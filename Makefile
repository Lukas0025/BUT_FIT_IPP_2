zip:
	mkdir tmpzip
	cp src/interpret/* ./tmpzip | true
	cp src/test/* ./tmpzip | true
	cp README.md ./tmpzip/readme2.md
	chmod +x ./tmpzip/*.php
	cd tmpzip && zip -r xpleva07.zip *
	cp tmpzip/xpleva07.zip ./
	rm -rf tmpzip

test: zip
	php src/test/test.php --directory ./spec/int-only --int-only --recursive --int-script src/interpret/interpret.py > testout.html
	./spec/is_it_ok.sh  xpleva07.zip tmpzip
	rm -rf tmpzip

clean:
	rm -rf xpleva07.zip
	rm -rf tmpzip