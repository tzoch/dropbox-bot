Dropbox Mirror Bot for Reddit

Dropbox files become unavaiable if they recieve too much traffic. This is
problematic for files that are posted to reddit where they may be accessed
by many people in a short period of time. This bot seeks to solve that problem
by searching for submissions that come from the dropbox domain. In this first
implementation, the bot will only focus on mirroring image files by
reuploading them to imgur. However, other versions could mirror other
filetypes such as videos (via youtube or vimeo), audio (via soundcloud), pdf,
txt or any other filetype that is posted frequently.

Basic Bot Functionality Outline:
1. Scrape both 
	 reddit.com/domain/dropbox.com
	 reddit.com/domain/dl.dropboxusercontent.com
   for submissions that contain a supported filetype
2. When a supported filetype is found, download the file
3. Reupload to the appropriate host depending on the filetype.
4. Post explanation of the  bot and a link to the mirror as a comment
   in the original submissions.
6. Delete the temporary files.
5. Continue searching for supported filetypes.   

USAGE
First, you must rename the sample_config.json file to config.json
Then, update the config.json to include your credentials.
