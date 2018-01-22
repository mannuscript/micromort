A thread is a set of posts
post_number = 1 will represent the main/starting post of the thread!

Fields:
Category: Category
Title: Title
updated_at : Posted/updated at datetime
user: Details of the poster 
    url: URL to the profile
    number_of_posts
    id : unique user_id

Thread_url : URL of the parent thread 

post : 
    content: actual content of the post (Html format)
    post_number: post_number=1 represents the main thread topic, 2 to N represent replies to the thread
    post_time : ...
    post_url: Every post has its own unique url, irrespective of thread's url

E.g.:
```{
    "category": "Campus Zone",
    "title": "\r\n\t Surviving NUS.\r\n\r\n",
    "updated_at": "10-11-2017 16:00:52",
    "user": {
        "url": "/users/521364/",
        "number_of_posts": "\r\n\t\t\t\t\tPosts: 12,306\r\n\t\t\t\t",
        "id": "Louislim"
    },
    "thread_url": "http://forums.hardwarezone.com.sg/nus-305/surviving-nus-3827077.html",
    "post": {
        "content": "<td class=\"alt1\" id=\"td_post_68529950\">\r\n\t\r\n\t\t\r\n\t\t\r\n\t\t\t<!-- icon and title -->\r\n\t\t\t<div class=\"smallfont\">\r\n\t\t\t\t\r\n\t\t\t\t<strong>Surviving NUS.</strong>\r\n\t\t\t</div>\r\n\t\t\t<hr size=\"1\" style=\"color:\">\r\n\t\t\t<!-- / icon and title -->\r\n\t\t\r\n\t\t\r\n\t\t<!-- message -->\r\n\t\t<div id=\"post_message_68529950\" class=\"post_message\">Hi,<br>\r\n<br>\r\nI havent managed to attend any camps so far and there arent many friends I know who is going to attend my course. I heard from others that many engineering students are just on their own all the way in school.<br>\r\n<br>\r\nI think I might jolly well end up the same as these students. So my question is- if I hardly know anyone, how am I supposed to find a project group if there are projects and stuff? They allocate randomly? <br>\r\n<br>\r\nAny advice is appreciated.</div>\r\n\t\t<!-- / message -->\r\n\t\r\n\t\t\r\n\t\t\r\n\t\t<div class=\"vbseo_buttons\" id=\"lkbtn_1.3827077.68529950\" style=\"width:auto; overflow:hidden;\">\r\n\r\n    <div class=\"alt2 vbseo_liked vbseo_like_own\" style=\" display:none;\"></div>\r\n\r\n</div>\r\n\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t</td>",
        "post_number": "1",
        "post_time": "23-07-2012, 11:28 AM",
        "post_url": "/68529950-post1.html"
    }
}'''