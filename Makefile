zip:
	mkdir tmpzip
	cp src/interpret/* ./tmpzip | true
	cp src/test/* ./tmpzip | true
	cp -r ./spec/int-only ./tmpzip/int-tests
	cp README.md ./tmpzip/readme2.md
	chmod +x ./tmpzip/*.php
	cd tmpzip && zip -r xpleva07.zip *
	cp tmpzip/xpleva07.zip ./
	rm -rf tmpzip

jexamxml:
	mkdir jexamxml
	cd jexamxml && wget http://www.a7soft.com/jexamxml.zip && \
	unzip jexamxml.zip

test-dir: zip
	mkdir tmpzip
	cp xpleva07.zip ./tmpzip
	cd ./tmpzip && unzip xpleva07.zip

test: test-dir
	php tmpzip/test.php --directory ./tmpzip/int-tests/ --int-only --recursive --int-script tmpzip/interpret.py > testout.html
	./spec/is_it_ok.sh  xpleva07.zip tmpzip
	rm -rf tmpzip

clean:
	rm -rf xpleva07.zip
	rm -rf tmpzip
	rm -rf jexamxml
	rm -rf */*/*.testout
	rm -rf */*/*.testrc
