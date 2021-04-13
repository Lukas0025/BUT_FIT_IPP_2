zip:
	mkdir tmpzip
	cp -r src/interpret/* ./tmpzip
	cp -r src/test/* ./tmpzip
	cp README.md ./tmpzip/readme2.md
	cd tmpzip && zip -r xpleva07.zip *
	cp tmpzip/xpleva07.zip ./
	rm -rf tmpzip

test: zip
	php src/test/test.php --directory ./spec/int-only --int-only --int-script src/interpret/interpret.py > testout.html
	./spec/is_it_ok.sh  xpleva07.zip tmpzip
	rm -rf tmpzip
