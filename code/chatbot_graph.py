from answer_search import *
from helper.preprocess import PreProcess

class ChatBotGraph:
    def __init__(self):
        self.searcher = AnswerSearcher()
        self.pp = PreProcess()

    # def chat_main(self, sent):
    #     answer = "Hello, I am XiaoMar Medical Assistant, I hope I can help you. If I don't answer it, I suggest you consult a professional doctor. I wish you a great body!"
    #     res_classify = self.classifier.classify(sent)
    #     if not res_classify:
    #         # print('='*50)
    #         return answer
    #     res_sql = self.parser.parser_main(res_classify)
    #     print('res_sql',res_sql)
    #     final_answers = self.searcher.search_by_dataframe()
    #     if not final_answers:
    #         print('='*50)
    #         return answer
    #     else:
    #         return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('User:')
        answer = handler.chat_main(question)
        print('XiaoMar:', answer)

