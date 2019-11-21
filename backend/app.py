from flask import Flask
import urllib.request
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import os
import time
from flask_cors import CORS, cross_origin
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import send_file

app = Flask(__name__)
cors=CORS(app)	
app.secret_key = "secret key"
ALLOWED_EXTENSIONS = set(['pdf'])
name_id_dict = dict() 
course_dict = [] 

@app.route('/courses')
def read_courses():
	global course_dict
	return json.dumps(course_dict)

@app.route('/courseinfo')
def courseinfo():
	global course_dict
	rid=request.args['id']
	for i in course_dict:
		if(i["id"]==int(rid)):
			return(json.dumps(i))
	return "NOT found"

@app.route('/return-files/')
def return_files_tut():
	thefile=request.args['file']
	try:
		return send_file('files/'+thefile, attachment_filename=thefile)
	except Exception as e:
		return str(e)


# @app.route('/open_pdf')
# def return_file():
# 	# open_pdf?fname
# 	fname = request.args['fname']
# 	return send_from_directory('files/', fname)

@app.route('/suggest')
def suggest():
	if request.method == 'GET':
		query_str = request.args['query']
		start_o = int(request.args['start'])
		end_o = int(request.args['end'])
		file_list = os.listdir("files")
		if(query_str == ""):
			if(len(file_list) >= end_o):
				return json.dumps(file_list[start_o: end_o])
			else:
				return json.dumps(file_list[start_o: len(file_list)+1])
		# print(file_list)
		res = []
		for i in file_list:
			if(i[:len(query_str)] == query_str):
				res.append(i)
		return json.dumps(res)


@app.route('/long_poll')
def wassup():
	global course_dict
	if request.method == 'GET':
		stat = os.stat("courses.txt")
		rtime = stat.st_mtime
		while(1):
			# rtime = float(request.get_json()['time'])
			stat = os.stat("courses.txt")
			mtime = stat.st_mtime
			if(rtime<mtime):
				# F = open("courses.txt","r")
				# fr = F.read()
				# temp = json.loads(fr)
				# F.close()
				rtime = mtime
				rid=request.args['id']
				for i in course_dict:
					if(i["id"]==int(rid)):
						return(json.dumps(i))

# @app.route('/upload')
# def upload_form():
# 	return render_template('upload.html')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fupload',methods=['POST'])
def flask_upload():
	global course_dict
	if request.method == 'POST':
			rid = request.form['id']
			if 'fileKey' not in request.files:
				flash('No file part')
				return redirect(request.url)
			file = request.files['fileKey']
			if file.filename == '':
				flash('No file selected for uploading')
				return "no file selected"#redirect(request.url)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join("files/", filename))
				for i in range(len(course_dict)):
					if(course_dict[i]["id"]==int(rid)):
						# print(i["documents"])
						course_dict[i]["documents"].append(filename)
						r = open("courses.txt","w")
						r.write(json.dumps(course_dict))
						r.close()
				return json.dumps("hello")


@app.route('/categorise', methods=['POST']) 
def categorise_file():	
	if request.method == 'POST':
		if 'fileKey' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['fileKey']
		if file.filename == '':
			flash('No file selected for uploading')
			return "no file selected"#redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print("done")
			file.save(os.path.join("", 'check.pdf'))
		else:
			flash('Allowed file type is only pdf')
			return redirect(request.url)

		def jaccard_similarity_(query, document):
			intersection = set(query).intersection(set(document))
			union = set(query).union(set(document))
			return len(intersection)/len(union)


		def cosine_similarity_(query,document):
			documents=(query,document)
			tfidf_vectorizer=TfidfVectorizer()
			tfidf_matrix=tfidf_vectorizer.fit_transform(documents)
			cs=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix)
			return cs[0][1]

		class pdfex:
			def __init__(self, fname):
				self.f_name = fname
				self.recognized_text = ""
				self.keywords = []

			def extract_text(self):
				pdf = wi(filename = self.f_name, resolution = 300)
				pdfImage = pdf.convert('jpeg')
				imageBlobs = []
				for img in pdfImage.sequence:
					imgPage = wi(image = img)
					imageBlobs.append(imgPage.make_blob('jpeg'))

				for imgBlob in imageBlobs:
					im = Image.open(io.BytesIO(imgBlob))
					text = pytesseract.image_to_string(im, lang = 'eng')
					self.recognized_text += text

			def get_tokens(self):
				tokenizer = RegexpTokenizer(r'\w+')
				tokens = tokenizer.tokenize(self.recognized_text)
				punctuations = ['(',')',';',':','[',']',',']
				stop_words = stopwords.words('english')
				keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
				self.keywords = ' '.join([str(elem) for elem in keywords])
				return ' '.join([str(elem) for elem in keywords])

		def most_prob_subject(test):
			j_sim={}
			cs_sim={}
			similarity={}
			for i in sub_words.keys():
				j_sim[i]= jaccard_similarity_(test, sub_words[i])
				cs_sim[i] = cosine_similarity_(test, sub_words[i])
				similarity[i]=(j_sim[i]+cs_sim[i])/2

			return max(similarity.keys(), key=(lambda k: similarity[k]))


		to_classify= "check.pdf"
		df = pd.read_csv('subject_classify_training.csv')


		tt = pdfex(to_classify)
		tt.extract_text()
		target_keywords = tt.get_tokens()


		#dictionary of subject:keywords
		sub_words ={}
		for i in df.values:
			if i[0] in sub_words.keys():
				sub_words[i[0]]+=" "+i[2]
			else:
				sub_words[i[0]]=i[2]
		global name_id_dict
		prediction = most_prob_subject(target_keywords)
		# return(json.dumps(prediction))
		return(json.dumps(name_id_dict[prediction]))

if __name__ == '__main__':
	# global course_dict
	# zzzz=[{"id":1,"name":"Operating System","credits":"4","description":"This course will introduce the core concepts of operating systems, such as processes and threads, scheduling, synchronization, memory management, file systems, input and output device management and security. The course will consist of assigned reading, weekly lectures, a midterm and final exam, and a sequence of programming assignments. The goal of the readings and lectures is to introduce the core concepts. The goal of the programming assignments is to give students some exposure to operating system code. Students are expected to read the assigned materials prior to each class, and to participate in in-class discussions.","image":"assets/linux.jpeg","documents":["Introduction.pdf","Syllabus.pdf"],"videos":["https://www.youtube.com/watch?v=2i2N_Qo_FyM","https://www.youtube.com/watch?v=QTQ8zym8Au0"]},{"id":2,"name":"Web Technologies","credits":"4","description":"The focus in this course is on the World Wide Web as a platform for interactive applications, content publishing and social services. The development of web-based applications requires knowledge about the underlying technology and the formats and standards the web is based upon. In this course you will learn about the HTTP communication protocol, the markup languages HTML, XHTML and XML, the CSS and XSLT standards for formatting and transforming web content, interactive graphics and multimedia content on the web, client-side programming using Javascript.","image":"assets/webt.jpeg","documents":["Introduction.pdf","Syllabus.pdf"],"videos":[]},{"id":3,"name":"Object Oriented Design","credits":"4","description":"Introduction to OOAD training begins by exploring advanced Object-Oriented (OO) concepts, like multiple inheritance, polymorphism, inner classes, etc. by building on the core OO concepts. The course then transitions from concept theory into object oriented design practices. The course concludes by examining design strategies such as noun-verb decomposition, user stories, use cases, Class-Responsibility-Collaboration (CRC) Cards, 4+1 architectural view, etc","image":"assets/oomd.jpg","documents":["Introduction.pdf","Syllabus.pdf"],"videos":["https://www.youtube.com/watch?v=2i2N_Qo_FyM","https://www.youtube.com/watch?v=QTQ8zym8Au0"]},{"id":4,"name":"Algoruthms and Data Structures","credits":"4","description":"Introduction to OOAD training begins by exploring advanced Object-Oriented (OO) concepts, like multiple inheritance, polymorphism, inner classes, etc. by building on the core OO concepts. The course then transitions from concept theory into object oriented design practices. The course concludes by examining design strategies such as noun-verb decomposition, user stories, use cases, Class-Responsibility-Collaboration (CRC) Cards, 4+1 architectural view, etc","image":"assets/oomd.jpg","documents":["Introduction.pdf","Syllabus.pdf"],"videos":["https://www.youtube.com/watch?v=2i2N_Qo_FyM","https://www.youtube.com/watch?v=QTQ8zym8Au0"]},{"id":5,"name":"Software Engineering","credits":"4","description":"Software engineering is a detailed study of engineering to the design, development and maintenance of software. Software engineering was introduced to address the issues of low-quality software projects. Problems arise when a software generally exceeds timelines, budgets, and reduced levels of quality.","image":"assets/oomd.jpg","documents":["Introduction.pdf","Syllabus.pdf"],"videos":["https://www.youtube.com/watch?v=2i2N_Qo_FyM","https://www.youtube.com/watch?v=QTQ8zym8Au0"]}]
	# zz = open("courses.txt", "w")
	# zz.write(json.dumps(zzzz))
	# zz.close()	
	x = open("courses.txt","r")
	course_dict = json.loads(x.read())
	# for i in name_id_dict:
	name_id_dict['WT'] = 2
	name_id_dict['SE'] = 5
	name_id_dict['OOMD'] = 3
	name_id_dict['OS'] = 1
	name_id_dict['ADA'] = 4
	app.run(host='0.0.0.0',port= 7000,debug=True, threaded=True)