### TODO

Wish List

1. Add support for more filetypes
2. Automate adding user to blacklist

Necessary Fixes

1. Fix imgur api authorization
2. Recognize differences in filesize limits
   to filetype differences
	* gifs are limited to 2mb anonymous, 5mb logged in
	* all other filetypes 20mb anonymous and logged in
		- but anonymous uploads are compressed to 1mb,
		  logged in compressed to 10 mb
3. Eliminate the need to check all of the 100 submissions
   before realizing that they are no new links from the
   dropbox domain
	* perhaps fetch 10 processed thing_id from the database,
	  and if 9 out of the first 10 submission thing_ids are also in the database, break the loop and go to sleep
