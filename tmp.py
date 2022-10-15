import subprocess
from typing import Tuple, Union
from danielutils import read_file, int_to_char, write_to_file, str_to_bytes, dict_to_json, json_to_dict
import re

# PATH = "C:\\Users\\User\\Desktop\\Programing\\VCS\\python\\midi-simplifier\\data\\output\\note.pdf"


# def bytes_to_string(b: bytes) -> str:
#     res = ""
#     for c in b:
#         res += int_to_char(c)
#     return res


# # s = """4å4»¬nð\x80Ûát\x93·\x7fÈn¨Ø>\x95§)\x8bËÌ\x99À\x08&Öb"ó~Õ¦¡huf\x9bfÇ>\x8asØ\x9dX}Ä#EºY¤÷\x91¸~¤\x08+ýMD\x87;¢ÃÕ§ã\x81\x88\x0eSD\x87¹O\x87¿&Pí¯!ÿ\x94©\x0fXÎú\x9c\r9ë\xad¬Õ\x82uKôã\x1bû@ç\x9cèòÜ©ê¬$¸B\x89\xa0õ\x0c£Go\x9ah1ÞÖ\x04ÞÊ[\x0cÖÖ\rOR¢æ\x80Ï\x17\x90Ó\x05©eÉ°\x1eÖ\x07\x93\x9bR\x83Emá²\x06õ^}\'à\x08tîØû¿Ù\x1c¡wìËnPgR·Ûå\x9d¢\x14\x15`À®\x0c¯<¸Éiqö\x11^»r\x876Êz1+)ëEUÛövh\x87®º®\x8eý\x0e\x87Ý\x01Nâ«ÀÈ6\x80\tÿ¤§\x16¯\x8657Nü\x16¯ú\x85\x13ß\x06eå6\x9dAxt«0ý\x05a\x92A³·Ôßð&?é\rþIL"\x10*¯Öb²´T¸\r\x18M{¤\x95Péq\x05\x08_Ú\x93N9½&?\x86É\x16évØn4ëI4\x01ÿ\x94Ù\x9b\x80éh\x02þïÌþéù¿ÂQê¯£Ä\x9fÃ½Ä2~¸\x86\x97©xò7ý\x85\x19ð(<·qî|\x95èG\x8fýÈ\x0fû\x1b?4´¼zYpùdõòÇa&Ìk\x9fóÑ&\x87\r\x07T\x82?\x00\x01\x02.«ËìZ¹§°\x0b\x0eÃé#\'>ôî\x12è\x1dB\\P\x18U`)°æ\x03Á.#\x81\x8fåÇ+hG\x8e=\x17r@k+±iMS\x97>:ÍJl\x9b(^ê¸ò£\x87§íuöz¨\x83}Ö}ì¾]ÞÆ@CèÝ\x93m\x1fÀ{À\x8f½\x9f¿[ø5\x10\x0b\x98m\x16Ð½¥}»è"¡õ_m»ZrõCý±ùØ\x07&å¬J*\x16Q\'|ôÝ\x1f¾\x0b&W\xad\x0f$?Q¼a\x1eö\x85+Z\x97ÿ.ó\x06f_\x14³\r1oj,z\x19öÂá½\x07Îxê\x7f\x1d\x9a\x16x\xa0\x98-±\x15a\x938ù\x8f\x7fUÐ\x9cÚ®\x065\x94B©\xadÔüLò¼Ù\x11°_qo}êþÆ^\x03!¨\x81&[\x93µé\x93\x96\x93\x9fÂ\x1fào³~\x10F\x82\x15ó¼\x15\x88MZvvÛYÝ\x19B\x07Ò8-¶\x87S\x93\x7f³ì©²®Òcp\x12>ëúè½Ã\x98yoiúèÛt}ôíZ1ÒÛ\x8b¡\x0c\x16¨,È¯)Ùå´q\x98\x80\x08}pïÞ\x83G²;6%§dl\x98yiÎg\x8aÞâ<"zúózkó\x88ÞÓßX\x90®TdïJ9.§³ê_:pðÀù7äàÕ\x02\x16È\x9c¢|\x8d|kyK\x9d\x82¾\x9eÉçõdJé÷O-{fcÉ¦¤gV\x9cyÿHÝ¡nÌë\x97e7ó\x87pYÖ\x97\x10R!\xad<³h}þª$<\x82%\'ò_\x87\x03ÐYµ/ÜÕüz7¼\x03çÖ4¯\x12w¬>]ò\x86~MArVj\x1a\x9c)\x7fE\x8b\x86\x01£Ãì4w.Ûµ\x00½QeU[TÀÚÄ\x12Z´¿<X÷æç_½ÃSûH\x95³Ò\x0bA\x08\x96ùKAP\x80@\x1d\x9eqV[Y\xa0\x83m\x84.\x0bè\x83r±@¹¼Ý\x9f|øö×/û\x9d^\x1f\x04\xa0j{e9\x08\x04\x1e>üÜ)MmÞÖ\xa0\x8a¼üBx!Ì\x80\xad¦\x02ØJh¾Kêóx|xÇ°9¬\x0e"LáWQ¬ÓÌá\x1d\x02ÌVÖ\x823Â*LH6\x16,\x84ñ\x18}r\x1a\x8bß\x03¼Tx\x80¢ù #]=¿ô\x85\x17\x16T¿&§\x97Ë\x1eÿýó\x9f\x7fþû7?\x95\x9f\x96ù\x8c\x1eF.tI\x19£\x91A\x9b\x05S¤\x8b\x9fO[°à\x85Îó(`ê\x03\x14gu@tp\x1cá§~C9\x1d\x0e¼æ\x80\x8buZ\x10\x06NX9\x16¢ÃjÅ\x89\x07(\x0bËZDT\x0e\x8b\x93%´0ä\x19aÈûü\x90÷\x11Æ\x94\x87(ÇMy\x0e\x947å\x1aårpnQ\x9eÕm\x16·u\x8dboÊcQ\x1e²à%É$ÊãL.\x94\x87\x9ffüä»\x84Õ½ÂHÄ0ü*Ü\x8b·w/\x15¸\x97Hø£È.~u¯L\x12Ù¤°JÆx*|ò\x88E½>\\Xª/5\x94iòò49%\x9b5éÅë\xa0\x18\x8a|°\x03ª±4\x04\x1bZZ\x1av×\x91\x97\x1bö×\x1f\x87z\x083\xa0&ôm\x05E\x10\xa05é\x89\'¨\x9aÃ\x87Z»\xa0\x0b\x0eåÖ¼\x84\x877\x85\x1fAyÜv\x9fÉ\x93~lyÓbX\x0cË\x0bÒ\x93MF;ã1¡\x15\x84\x11âVlb\x9dÆ\x0cÎ¡ÑÆ}Mµu\x1eßñ*¼"""
# res = []
# skip = False
# lines = read_file(PATH, True)
# for i, line in enumerate(lines):
#     line = bytes_to_string(line)
#     if re.search(r"<</Type/Annot", line):
#         skip = True
#         continue
#     if re.search(r"^(\/URI\(textedit)", line):
#         skip = False
#         continue
#     if not skip:
#         res.append(line)
# write_to_file(PATH.replace("note.pdf", "note2.pdf"), res)
d = dict()
d[1] = 1
d[2] = [1, 2, 3, 4]


def dict_to_lines(d) -> list[str]:
    return [f"{v}\n" for v in dict_to_json(d).split("\n")]


write_to_file("j.json", dict_to_lines(d))
print(*read_file("j.json"))
