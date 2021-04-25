#  DEFINE RULE BASE:
# 	+ Check question:
# 	+ Random intent:
# 	+ Yes/No question:

# Check question

#  DEFINE RULE BASE:
# 	+ Check question:
# 	+ Random intent:
# 	+ Yes/No question:

# Check question

# list_question_signal = [" hả ", "chứ", "có biết", "phải không", "đâu", "là sao", "nào", "khi nào", "nơi nào", "không ạ", "k ạ", "là sao", "nữa vậy", "chưa á", "ko ạ", "sao ạ", "chưa ạ", "sao vậy", "không vậy", "k vậy", "ko vậy", "chưa vậy", "thế", " nhỉ ", " ai", " ai ", "ở đâu", "ở mô", "đi đâu", "bao giờ",
#                         "bao lâu", "khi nào", "lúc nào", "hồi nào", "vì sao", "tại sao", "thì sao", "làm sao", "như nào", "thế nào", "cái chi", "gì", "bao nhiêu", "mấy", "?", " hả ", "được không", "được k", "được ko", "vậy ạ", "nào vậy", "nào thế", "nữa không", "đúng không", "đúng k", "đúng ko", "nữa k", "nữa ko", "nào ấy", "nào ạ"]
# list_question_signal_last = ["vậy", "chưa",
#                              "không", "sao", "à", "hả", "nhỉ", "thế"]
# list_object = ["bạn", "cậu", "ad", "anh", "chị", "admin", "em", "mày", "bot"]
# list_subject = ["mình", "tôi", "tớ", "tao", "tui", "anh", "em"]
list_verb_want = ["hỏi", "biết", "xin","cần","nhờ","tư vấn","muốn","yêu cầu","thông tin về ",
"biết về","hỏi về ","tìm hiểu về","là gì","gì","cách","truy vấn","lấy ra","tìm hiểu",
"hiểu về","làm sao","mún","làm thế nào","làm gì"]
# list_verb_have = ["có", "được"]

# Random intent

list_hello_notification = ["hello", "chào", "helo","tôi cần tư vấn","tôi cần hỗ trợ",
                           "xin chào", 'chào bác sĩ', 'chào bạn', 'chào bot', 'alo']
list_done_notification = ["bye", "tạm biệt", "bai",
                          "gặp lại", 'pp', 'goodbye', 'bye bye', 'bai bai']
list_thanks_notification = ["cảm ơn", "tks", "thanks", 'thank', 'cảm ơn bác sĩ',
                            'cảm ơn bot', 'cảm ơn nhiều', 'cảm ơn nhiều ạ', 'cảm ơn ạ', 'thank you']
list_anything_notification = ["sao cũng được", "gì cũng được", "anything", "s cũng được",
                              'j cũng được', "không biết", "k biết", "ko biết", "không nhớ", "ko nhớ", "k nhớ", "không rõ",
                              "k rõ", "ko rõ", "cũng được", "cũng ok", "cũng không sao", "cũng dc", "cũng k sao", "cũng ko sao"]

# Yes/No question

list_agree_notification = ['yes', 'ok', 'đúng rồi',
                           'đúng', 'chắc vậy', 'chính xác', 'phải rồi']
list_disagree_notification = ['không phải', 'no', 'sai rồi', 'sai']


class QuestionChecker:
    def __init__(self):
        self.mess = 'None'

    def is_random_intent(self, message):
        if message in list_hello_notification:
            return 'Hello human :)'
        if message in list_done_notification:
            return "Chúc bạn một ngày tốt lành"
        if message in list_thanks_notification:
            return "Chúc bạn một ngày tốt lành"
        if message in list_anything_notification:
            return "Tôi giúp được gì cho bạn ? "
        return "No Random"

    def is_question(self, message):
        for syl in list_verb_want:
        	if message.lower().find(syl) != -1:
		        return True
        return False
	# def catch_biz_rand_intent(self, biz, rand):
	# 	"""
	# 	classify between business intent & random intent\
	# 	-----|-----|-----
	# 	rand | biz | res
	# 	-----|-----|-----
	# 	  0  |  0  | None
	#     -----|-----|-----
	#       0  |  1  | biz
	#     -----|-----|-----
	#       1  |  0  | rand
	#     -----|-----|-----
	#       1  |  1  | biz
	#     -----|-----|-----
	# 	"""
    #     if rand == False and biz == False:
    #         return None
    #     if biz == True:
    #         return biz
	# 	return rand

	# def final_intent(self):
	# 	"""
	# 	4 intent available:
	# 		+ random intent
	# 		+ biz intent
	# 		+ other intent
	# 		+ not intent
	# 	"""
	# 	# Step 1: check question

	# 	if self.check_question(self.mess):
	# 		return self.catch_biz_rand_intent()
	# 	else:
    #         return 'not_intent'
