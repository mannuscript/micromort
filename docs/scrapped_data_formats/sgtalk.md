A thread is a set of posts
post_number = 1 will represent the main/starting post of the thread!

Fields:
Category: Category
Title: Title
updated_at : Posted/updated at datetime
user: Details of the poster 
    url: URL to the profile
    reputation: of the user at the time of crawling the page
    Name & id : Name and user_id

Thread_url : URL of the parent thread 
post : 
    content: actual content (Html format)
    post_number: post_number=1 represents the main thread topic, 2 to N represent replies to the thread
    post_time : ...
    post_url: Every post has its own unique url, irrespective of thread's url

E.g.:
```
{
    "category": "Market Talk",
    "title": "KBW: Desmond had volunteered for the SMRT job, not parachuted in",
    "updated_at": "08-11-2017 13:54:03",
    "user": {
        "url": "http://sgtalk.org/mybb/User-Tangsen",
        "reputation": "9",
        "name": "\r\n\t\t\tFirst Class Elite",
        "id": "Tangsen"
    }, 
    "thread_url": "http://sgtalk.org/mybb/Thread-KBW-Desmond-had-volunteered-for-the-SMRT-job-not-parachuted-in",
    "post": {
        "content": "<td><span class=\"smalltext\"><strong><div class=\"float_right\"></div></strong></span>                        \r\n\t\t\t<div id=\"pid_2520272\"   class=\"post_body\">\r\n\t\t\t\tVolunteered? I can volunteer also, so hire me also?<br>\nHe has any track records, experience?<br>\nHe paper general, can he run a train service?\r\n\t\t\t</div>\r\n\t\t\t\r\n\t\t\t\r\n\t\t\t<div style=\"text-align: right; vertical-align: bottom;\" id=\"post_meta_2520272\">\r\n\t\t\t\t<div id=\"edited_by_2520272\"></div>\r\n\t\t\t\t\r\n\t\t\t</div>\r\n\t\t        </td>",
        
        "post_number": "#10",
        "post_time": "Yesterday 2:28 PM",
        "post_url": "Thread-KBW-Desmond-had-volunteered-for-the-SMRT-job-not-parachuted-in?pid=2520272#pid2520272"
    }
 }
 ```