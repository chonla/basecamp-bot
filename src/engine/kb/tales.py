import random
import time


class Tales:
    def __init__(self):
        random.seed(time.time())

    def get_one(self):
        tales = [
            '''ชายชราผู้หนึ่งมีฐานะยากจน สมบัติทั้งหมดที่เขามีก็คือบ้านเก่าๆ หลังหนึ่งกับแม่ห่านอีกตัวหนึ่งเท่านั้น แม่ห่านจะออกไข่วันละฟองเพื่อให้เขานำไปขายที่ตลาดทุกวัน อยู่มาวันหนึ่งแม่ห่านนึกสงสารจึงออกไข่ทองคำฟองหนึ่งให้แก่ชายชราชายชราดีใจมาก รีบนำไข่ทองคำไปขายได้เงินมามากมายและทำให้ฐานะดีขึ้น แต่ชายชรายังไม่พอใจ เกิดความโลภอยากจะได้ไข่ทองคำหลายๆ ใบในคราวเดียวกัน

           ชายชราคิดว่าในท้องห่านต้องมีไข่ทองคำเหลืออยู่อีกมาก วันหนึ่งเขาจึงแอบย่องเข้าไปในเล้าห่าน แล้วเอามีดที่เตรียมไว้ผ่าท้องห่านทันที แต่อนิจจา นอกจากจะไม่พบไข่ทองคำเลยสักใบในท้องห่านแล้ว แม่ห่านก็ต้องมาตายลงอีกนับแต่นั้นเป็นตันมา ชายชราผู้โลภมากไม่มีทั้งห่าน หรือแม้แต่ไข่ห่านสักใบให้นำไปขายอีกต่อไป''',
           '''สุนัขเฝ้าบ้านตัวหนึ่งมีนิสัยดุร้าย ชอบไล่กัดผู้คนที่เดินผ่านไปมา สร้างความรำคาญให้กับเพื่อนบ้านในละแวกนั้น เมื่อเจ้าของสุนัขถูกต่อว่ามากๆ จึงเอาโซ่ล่ามสุนัขไว้กับท่อนไม้หน้าบ้าน แต่เจ้าสุนัขเกเรกลับคิดว่า เจ้านายให้ท่อนไม้เป็นรางวัลตอบแทนความดีที่มันทำตัวดุร้ายอย่างนั้น มันจึงชอบยืนชูคออยู่ข้างท่อนไม้ด้วยความภาคภูมิใจ และถ้ามีสุนัขตัวใดเดินผ่านมา มันก็จะพูดอวดเสียงดังว่า 

        "สุนัขอย่างพวกเจ้า คงไม่มีวันได้รางวัลเป็นท่อนไม้ที่แข็งแรง เหมือนอย่างที่ข้าได้จากเจ้านายของข้าหรอก ฮ่า ฮ่า ฮ่า"

        เหตุการณ์เป็นอย่างนี้เรื่อยมา จนวันหนึ่ง เจ้าสุนัขเกเรก็หัวเราะไม่ออกเมื่อสุนัขชราตัวหนึ่งที่ผ่านมากล่าวแก่มันว่า

        "ถ้าเจ้าไม่คิดเข้าข้างตัวเองเกินไปเจ้าจะรู้นานแล้วว่า ทั้งท่อนไม้และโซ่ที่ล่ามเจ้าไว้นี้ มิได้เป็นรางวัลแก่การทำดีของเจ้าหรอก แต่มันคือเครื่องประจานความเกเรดุร้ายของเจ้าต่างหาก"'''
        ]
        return tales[random.randint(0, len(tales) - 1)]
