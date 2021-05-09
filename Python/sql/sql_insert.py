import re
event_texts = '''Năm thánh lập 1995:Nuôi các trẻ ở vùng sâu, xa ăn học và hỗ trợ chỗ ở
Năm 1998:Bắt đầu nhận nuôi 3 trẻ sơ sinh bỉ bỏ rơi đầu tiên Xây nhà 923/7
Năm 2000:Sau năm năm hoạt động số lượng trẻ lên tới 20 trẻ
Năm 2004:Sơ Yên tổ chức cho trẻ đi nghỉ hè ở Phan Thiết
Năm 2005:Đến thời điểm này đã có 5 trẻ giúp trong hoàn cảnh khó khăn bước vào học nghề và ra ngoài tự lập, Số lượng trẻ thời điểm này đã lên tới 50 trẻ
Năm 2010:Đây là thời điểm có số lượng trẻ sơ sinh lên đến 10 cháu, Giai đoạn này tổng số lượng trẻ là 60 cháu, Đánh dấu cột mốc 15 năm hoạt động của mái ấm
Năm 2012:Được các ân nhân cho mượn thêm 2 ngôi nhà liền kề để tiện cho việc sinh hoạt cho các cháu, Giai đoạn này có thêm 10 cháu được giúp đỡ ra ngoài tự lập, học nghê và đi làm
Năm 2015:Số lượng các cháu đến thời điểm hiện tại là 40 trẻ. Đã trả trẻ còn người thân về với gia đình, Mái ấm lúc này được quy hoạch lại để chuẩn bị cho việc cấp phép hoạt động.
Năm 2016:Mái ấm được cấp phép hoạt động, Trẻ tới tuổi được làm chứng mình nhân dân và vao đại học, Tiến hành thủ tục nhập khẩu cho trẻ
Năm 2017 - 2018:Xây dựng lại mái ấm, Khánh thành ngày 4/8/2018
Năm 2019:Ký đối tác với trường Đại Học Kinh Tế Tài Chính
Năm 2020:Cột mốc 25 năm với 3 trẻ sơ sinh đầu tiên ra trường và đi làm.'''
rule_texts = '''NỘI QUY MÁI ẤM::
1. Giờ giấc đúng quy định (Đi về đúng giờ, tối 9h45 đóng cửa…)
2. Quần áo nghiêm chỉnh, tác phong đúng đắn.
3. Kính trên nhường dưới
4. Yêu thương phục vụ (giúp đỡ lẫn nhau)
5. Đi thưa về trình
6. Minh bạch trong mọi vấn đề
7. Không trộm cắp
8. Không làm các hành vi vi phạm pháp luật.
::DIỄN GIẢI NỘI QUY MÁI ẤM::
1. Giờ giấc: 8h30 đọc kinh tối
9h45 đóng cổng tối. Những người đi làm trễ (Đạt, Hương, Phương, Ân)
sẽ được phát chìa khoá.
2. Quần áo nghiêm chỉnh, tác phong đúng đắn: đi học về đồ dơ bỏ giặt, quần áo
sau khi phát xếp ngăn nắp gọn gàng.
- Giầy dép để đúng nơi quy định nếu không để đúng sau 3 lần nhắc nhở sẽ
đem bỏ rác. Nhắc quá 3 lần sẽ họp cảnh cáo trước tập thể và nhờ chính
quyền can thiệp.
- Thực đẩy đủ các việc được giao như: dọn dẹp phòng, đi vệ sinh phải dội,
tắm xong phải để quần áo vào sọt, sàn nhà luôn sạch và khô, rửa chén,
quyét nhà.
- Không vẽ bậy lên tường, không đi chân đất ra đường, không mang dép
trong nhà và lên lầu.
- Quần áo sạch sẽ, đóng thùng ngăn nắp gọn gàng, không mặc đồ hở hang.
- Không nấu nướng ban đêm. Không tự ý tổ chức, tụ tập ăn nhậu ban đêm.
- Không được vào phòng người khác để sinh hoạt cá nhân.
3. Kính trên nhường dưới: Biết vâng lời người lớn, ngoan ngoãn, lễ phép. Không
sai khiến, chèn ép, bạo hành các em dưới mình (không sai các em phục vụ
riêng cho bản thân mình).
4. Yêu thương phục vụ: Biết yêu thương nhau, không đánh nhau, cãi nhau, chửi
thề, làm gương xấu, giúp đỡ lẫn nhau.
5. Đi thưa về trình: Đi học theo lịch, đi về cho đúng giờ. Trường hợp ngoại lệ
phải báo với người lớn.
6. Minh bạch trong mọi vấn đề: Thông báo cho người quản lí biết nơi làm việc,
giờ làm việc, lương….để có sự giám sát, tránh xảy ra tình trạng bị bóc lột sức
lao động.
7. Không trộm cắp: Không được lục tủ, lấy đồ của nhau. Không được cậy ổ khoá,
đập cửa.
8. Không làm các hành vi vi phạm pháp luật:
- Không thực hiện các hành vi dâm dục
- Không tiếp tay thực hiện các hành vi phạm pháp luật như cầm giúp, giữ
giùm, giao giúp bạn, người xa lạ các chất trái phép, vũ khí….
::NẾU KHÔNG THỰC HIỆN NHỮNG ĐIỀU NÊU TRÊN::
- Sau 3 lần nhắc nhở sẽ họp cảnh cáo trước tập thể lần thứ 1, lần 2. Lần thứ 3
mời chính quyền chứng kiến, can thiệp. Sau những lần vi phạm. Sẽ giao
cho cơ quan có thẩm quyền xử lí
- Những điều làm trái pháp luật thì CÁ NHÂN đủ tuổi theo pháp luật quy
đinh phải tự chịu trách nhiệm. Mái ấm không bảo lãnh, không đóng
phạt….và những gì liên quan khi có vấn đề khác xảy ra.'''
for index, text in enumerate(event_texts.split("\n"), 1):
    sql = f"INSERT INTO event (e_id, e_title, e_text)\nVALUES ('{index}', '{text.split(':')[0]}', '{text.split(':')[1]}');\n"
    print(sql)
i = 0
for index, text in enumerate(rule_texts.split("::"), 1):
    if index % 2 == 0:
        for item in list(filter(None, map(lambda s: s.strip(), re.split(r'(?:\n\d. )', text)))):
            i += 1
            sql = f"INSERT INTO rule_texts (rule_text_id, rule_id, rule_text)\nVALUES ('{i}', '{index // 2}', '{item}');\n"
            # print(sql)
    else:
        sql = f"INSERT INTO rule (rule_id, rule_title)\nVALUES ('{index // 2 + 1}', '{text}');\n"
        # print(sql)
