import copy
from fractions import Fraction
from typing import Callable, Any, Union, Optional
from .probability_expression import ProbabilityExpression
from ..protocols import Evaluable, Equatable
from ..operator import Operator
from ....data_structures import BinarySyntaxTree as BST

def _create_operator(op: Operator, reverse: bool = False) -> Callable[['AccumulationExpression', Any], Evaluable]:
        def operator(self, other) -> Evaluable:
            lhs, rhs = self, other
            if reverse:
                lhs, rhs = rhs, lhs
            if isinstance(other, (int, float, Fraction)) and op in Operator.order_operators():
                rhs_expr = ProbabilityExpression(lhs.lhs, op, other) if op in Operator.inequalities() else ProbabilityExpression(other)
                return AccumulationExpression(lhs, Operator.AND, rhs_expr)
            raise NotImplementedError("Not Implemented")

        return operator

class AccumulationExpression(Evaluable):
    @staticmethod
    def _to_leaf(value: Any) -> BST.Node:
        if isinstance(value, BST.Node):
            return value
        return BST.Node(value)

    @staticmethod
    def _probability_expression_to_nodes(expr: ProbabilityExpression) -> BST.Node:  # type:ignore
        if expr.op is None:
            return AccumulationExpression._to_leaf(expr.lhs)
        return BST.Node(
            expr.op,
            AccumulationExpression._to_leaf(expr.lhs),
            AccumulationExpression._to_leaf(expr.rhs),
        )


    @staticmethod
    def _expression_intersection(expr1: ProbabilityExpression, expr2: ProbabilityExpression) -> Fraction:
        if expr1.is_equal(expr2):
            return expr1.evaluate()

        a = expr1.rhs
        op1 = expr1.op
        b = expr2.rhs
        op2 = expr2.op
        X = expr1.lhs
        if op1 in Operator.greater_than_inequalities() and op2 in Operator.less_than_inequalities():
            return X.between(a, b, op1, op2)

        if op1 in Operator.greater_than_inequalities() and op2 in Operator.greater_than_inequalities():
            op = op1
            if op2 == Operator.GT:
                op = op2
            return X.evaluate(max(a, b), op)

        if op1 in Operator.less_than_inequalities() and op2 in Operator.less_than_inequalities():
            op = op1
            if op2 == Operator.LT:
                op = op2
            return X.evaluate(min(a, b), op)

        if op1 in Operator.equalities() and op2 in Operator.equalities():
            return Fraction(0, 1)

        if op1 in Operator.equalities():
            return expr1.evaluate()
        return expr2.evaluate()

    def __init__(self, lhs: ProbabilityExpression, op: Operator, rhs: ProbabilityExpression) -> None:
        l = AccumulationExpression._probability_expression_to_nodes(lhs)
        r = AccumulationExpression._probability_expression_to_nodes(rhs)
        root = BST.Node(op, l, r)
        self._tree = BST(root)

    _eq_operator = _create_operator(Operator.EQ)
    _ne_operator = _create_operator(Operator.NE)
    _gt_operator = _create_operator(Operator.GT)
    _ge_operator = _create_operator(Operator.GE)
    _lt_operator = _create_operator(Operator.LT)
    _le_operator = _create_operator(Operator.LE)

    def __eq__(self, other) -> bool:
        if isinstance(other, AccumulationExpression):
            return self.is_equal(other)
        return self._eq_operator(other)  # type:ignore[return-value]

    def __ne__(self, other) -> bool:
        if isinstance(other, AccumulationExpression):
            return not self.is_equal(other)
        return self._ne_operator(other)  # type:ignore[return-value]

    def __gt__(self, other):
        return self._gt_operator(other)

    def __ge__(self, other):
        return self._ge_operator(other)

    def __lt__(self, other):
        return self._lt_operator(other)

    def __le__(self, other):
        return self._le_operator(other)

    def __bool__(self) -> bool:
        if self._tree.root.data != Operator.EQ:
            return False

        def node_to_equatable(n: BST.Node) -> Equatable:  # type:ignore
            if n.depth() == 2:  # type:ignore
                return ProbabilityExpression(n.left.data, n.data, n.right.data)  # type:ignore
            pass

        if (d := self._tree.depth()) == 3:
            return node_to_equatable(self._tree.root.left).is_equal(node_to_equatable(self._tree.root.right))

        return NotImplemented

    def __reversed__(self) -> 'AccumulationExpression':
        return self.reverse()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lhs={self._tree.root.left}, op={self._tree.root.data}, rhs={self._tree.root.right})"

    def is_equal(self, other) -> bool:
        if not isinstance(other, AccumulationExpression):
            return False
        from ..conditional_variable import ConditionalVariable
        # I have to create a custom comparer because the BST can't (and shouldn't) know to compare using
        # ConditionalVariable.is_equal
        def are_nodes_equal(a: Any, b: Any) -> bool:
            if not (isinstance(a, BST.Node) and isinstance(b, BST.Node)):
                if a is None and b is None:
                    return True
                return False
            if isinstance(a.data, Operator) and isinstance(b.data, Operator):  # type:ignore
                if not (a.data == b.data):  # type:ignore
                    return False
            elif isinstance(a.data, ConditionalVariable) and isinstance(b.data, ConditionalVariable):  # type:ignore
                if not a.data.is_equal(b.data):  # type:ignore
                    return False
            else:
                return a.data == b.data  # type:ignore

            return are_nodes_equal(a.left, b.left) and are_nodes_equal(a.right, b.right)  # type:ignore

        return are_nodes_equal(self.standardize()._tree.root, other.standardize()._tree.root)

    def evaluate(self) -> Fraction:
        if not self._is_valid_tree():
            raise AttributeError("Expression is not valid")
        root = self._tree.root
        if root.data == Operator.EQ:
            return self._evaluate_equality(root)
        if (d := self._tree.depth()) == 3:
            # example: a < X < b
            # =>       ____&____          1
            #         /         \
            #     ___<___     ___<___     2
            #    a       X   X       b    3
            # but actually it is ordered differently
            # =>       ____&____          1
            #         /         \
            #     ___>___     ___<___     2
            #    X       a   X       b    3
            a = self._tree.root.left.right.data
            op1 = self._tree.root.left.data
            b = self._tree.root.right.right.data
            op2 = self._tree.root.right.data
            X = self._tree.root.left.left.data
            Y = self._tree.root.right.left.data
            lhs = ProbabilityExpression(X, op1, a)
            rhs = ProbabilityExpression(Y, op2, b)
            main_operator = self._tree.root.data
            if X is Y:
                if main_operator == Operator.AND:
                    return AccumulationExpression._expression_intersection(lhs, rhs)
                numerator: Fraction = AccumulationExpression._expression_intersection(lhs, rhs)
                denominator: Fraction = rhs.evaluate()
                return numerator / denominator
            if X.is_dependent(Y):
                raise NotImplementedError("This part is not implemented yet")
            raise NotImplementedError("Illegal State?")

        # example: a < X < Y < b
        raise NotImplementedError("This part is not implemented yet")

    @staticmethod
    def _leaf_value(node: BST.Node) -> Any:
        return node.data

    def _evaluate_equality(self, root: BST.Node) -> Fraction:
        from ..conditional_variable import ConditionalVariable

        left = root.left
        right = root.right
        if left is None or right is None:
            raise AttributeError("Expression is not valid")

        right_value = self._leaf_value(right)
        if isinstance(left.data, Operator) and left.left is not None and left.right is not None:
            lhs_val = self._leaf_value(left.left)
            rhs_val = self._leaf_value(left.right)
            if isinstance(lhs_val, ConditionalVariable):
                variable = lhs_val
                operand = rhs_val
                if left.data == Operator.ADD:
                    target = right_value - operand
                elif left.data == Operator.SUB:
                    target = right_value + operand
                else:
                    raise NotImplementedError("This part is not implemented yet")
                return variable.evaluate(target, Operator.EQ)
            if isinstance(rhs_val, ConditionalVariable):
                variable = rhs_val
                operand = lhs_val
                if left.data == Operator.ADD:
                    target = right_value - operand
                elif left.data == Operator.SUB:
                    target = operand - right_value
                else:
                    raise NotImplementedError("This part is not implemented yet")
                return variable.evaluate(target, Operator.EQ)

        left_value = self._leaf_value(left)
        if isinstance(right.data, Operator) and right.left is not None and right.right is not None:
            lhs_val = self._leaf_value(right.left)
            rhs_val = self._leaf_value(right.right)
            if isinstance(lhs_val, ConditionalVariable):
                variable = lhs_val
                operand = rhs_val
                if right.data == Operator.ADD:
                    target = left_value - operand
                elif right.data == Operator.SUB:
                    target = left_value + operand
                else:
                    raise NotImplementedError("This part is not implemented yet")
                return variable.evaluate(target, Operator.EQ)
            if isinstance(rhs_val, ConditionalVariable):
                variable = rhs_val
                operand = lhs_val
                if right.data == Operator.ADD:
                    target = left_value - operand
                elif right.data == Operator.SUB:
                    target = operand - left_value
                else:
                    raise NotImplementedError("This part is not implemented yet")
                return variable.evaluate(target, Operator.EQ)

        if isinstance(left_value, ConditionalVariable):
            return left_value.evaluate(right_value, Operator.EQ)
        if isinstance(right_value, ConditionalVariable):
            return right_value.evaluate(left_value, Operator.EQ)
        raise AttributeError("Expression is not valid")

    def duplicate(self) -> 'AccumulationExpression':
        return copy.deepcopy(self)

    def reverse(self) -> 'AccumulationExpression':
        res = self.duplicate()
        res._tree = res._tree.reverse()
        return res

    def standardize(self) -> 'AccumulationExpression':
        for n in self._tree.traverse(self._tree.TraversalMode.Middle):
            if n is self._tree.root:
                break
            if isinstance(n.data, Operator):
                if n.data in Operator.greater_than_inequalities():
                    return self.reverse()
        return self.duplicate()

    def _is_valid_tree(self) -> bool:
        q = [self._tree.root]
        i = 0
        while i < len(q):
            if isinstance(q[i], BST.Node):
                if not isinstance(q[i].data, Operator):
                    if not q[i].is_leaf:
                        return False
                else:
                    q.append(q[i].left)
                    q.append(q[i].right)
            i += 1
        return True


__all__ = [
    'AccumulationExpression'
]
