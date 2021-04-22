"""
 DEFINE RULE BASE:
	+ Check question:

	+ Random intent:

	+ Yes/No question:
"""

## Check question

list_question_signal = [" hả ","chứ","có biết","phải không","đâu","là sao","nào","khi nào","nơi nào","không ạ","k ạ","là sao","nữa vậy","chưa á","ko ạ","sao ạ","chưa ạ","sao vậy","không vậy","k vậy","ko vậy","chưa vậy","thế"," nhỉ "," ai"," ai ","ở đâu","ở mô","đi đâu","bao giờ","bao lâu","khi nào","lúc nào","hồi nào","vì sao","tại sao","thì sao","làm sao","như nào","thế nào","cái chi","gì","bao nhiêu","mấy","?"," hả ","được không","được k","được ko","vậy ạ","nào vậy","nào thế","nữa không","đúng không","đúng k","đúng ko","nữa k","nữa ko","nào ấy","nào ạ"]
list_question_signal_last = ["vậy","chưa","không","sao","à","hả","nhỉ","thế"]
list_object = ["bạn","cậu","ad","anh","chị","admin","em","mày","bot"]
list_subject = ["mình","tôi","tớ","tao","tui","anh","em"]
list_verb_want = ["hỏi","biết","xin"]
list_verb_have = ["có","được"]

## Random intent

list_hello_notification = ["hello","chào","helo"]
list_done_notification = ["bye","tạm biệt","bai","gặp lại",'pp']
list_thanks_notification = ["cảm ơn","tks","thanks",'thank']
list_anything_notification = ["sao cũng được","gì cũng được","anything","s cũng được",\
    'j cũng được',"không biết","k biết","ko biết","không nhớ","ko nhớ","k nhớ","không rõ",\
        "k rõ","ko rõ","cũng được","cũng ok","cũng không sao","cũng dc","cũng k sao","cũng ko sao"]

## Yes/No question

list_agree_notification = ['yes','ok','đúng rồi','đúng','chắc vậy','chính xác','phải rồi']
list_disagree_notification = ['không phải','no','sai rồi','sai']

class CatchIntent():
	"""
	catch user's intent from message input
	"""
	def __init__(self,message):
		"""
		init attribute

		"""
		self.mess = message

	def check_question(self):
		"""
		check question use rule-based

		return:
			+ True if message is question
		"""

	def catch_biz_rand_intent(self):
		"""
		classify between business intent & random intent\

		-----|-----|-----
		rand | biz | res
		-----|-----|-----
		  0  |  0  | None
	    -----|-----|-----
	      0  |  1  | biz
	    -----|-----|-----
	      1  |  0  | rand
	    -----|-----|-----
	      1  |  1  | biz
	    -----|-----|-----  
		"""
		return 


	def final_intent(self):
		"""
		4 intent available:
			+ random intent
			+ biz intent
			+ other intent
			+ not intent
		"""
		## Step 1: check question

		if self.check_question(self.mess):
			return self.catch_biz_rand_intent()

		else:
			return 'not_intent'
	