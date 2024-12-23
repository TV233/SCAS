from snownlp import sentiment
sentiment.train('venv\\Lib\\site-packages\\snownlp\\sentiment\\neg.txt','venv\\Lib\\site-packages\\snownlp\\sentiment\\pos.txt')
sentiment.save('sentiment.marshal')

