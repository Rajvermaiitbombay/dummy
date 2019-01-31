var username =""; 
 
 function send_message(message){


	var prevMsg = $("#container_").html();
	
		$("#container_").html(prevMsg +
			 " <span class= 'current_message'>"+ "<span class = 'Bot'> Bot :  </span>" 
			  + message +"</span>" + "<br>");
		$(".current_message").hide();
		$(".current_message").delay(500).fadeIn();
		$(".current_message").removeClass("current_message");

   }


 function get_username(){
 send_message("Hello , What is your name ?");
 }
	 
   function ai(message){
		  if ((username.length < 3) && (message.length>=3)){

			var l = $("#container_").html();
			username = message;
			send_message("Nice to meet you " + username + " , How are you ? ");
			}
		  else if ((username.length<3)&&(message.length<3)) {
		    send_message("Would you mind telling me your name ? ");
			}

		  else if(message.toLowerCase().indexOf("how are you")>=0){
			send_message("Thanks ! I am good . What would you like to know about sololearn ? ");
			}

		  else if(((message.toLowerCase().indexOf("fine")>=0)||(message.toLowerCase().indexOf("good")>=0)||(message.toLowerCase().indexOf("excellent")>=0)  ) && (message.toLowerCase().indexOf("how are you?")==-1)){
			send_message("Glad to hear that . What would you like to know about sololearn ? ");
			}

		  else if (message.length<3){
			send_message("Won't you like to talk to me ?");
			}

		  else if((message.toLowerCase().indexOf("what can you tell ")>=0) && (message.toLowerCase().indexOf("sololearn")>=0))
			{
			send_message("I know about sololearn's policy reguarding the following  \
				<br> ===============================================================================<br>\
					 |                   <span style = 'margin-left:300px;'>  Sololearn Guidelines </span>  <br>     \
					 ================================================================================<br> \
					 <ul>    \
					 <li> CONTENT CREATION </li>  \
					 <li> PERSONAL ABUSE  </li> \
					   <li>  Q&A DISCUSSIONS  </li>\
						<li> RIGHT TO POST  </li> \
						<li>CONTENT OWNERSHIP </li> \
					 </ul>  <br> \
					  ==================================================================================<br>\
			   . Which one would you like to know about ?"  );
			}

		  else if((message.toLowerCase().indexOf("what")>=0) && (message.toLowerCase().indexOf("sololearn")==-1))
			{
			send_message("About what you want to know ?");

			}

		  else if (((message.toLowerCase().indexOf("i")>=0)||(message.toLowerCase().indexOf("what")>=0))&&((message.toLowerCase().indexOf("know")>=0)&& message.toLowerCase().indexOf("sololearn")>=0)){

			send_message("I know about sololearn's policy reguarding the following  \
				 <br> ===============================================================================<br>\
				      |                   <span style = 'margin-left:300px;'>  Sololearn Guidelines </span>  <br>     \
					  ================================================================================<br> \
					  <ul>    \
					  <li> CONTENT CREATION </li>  \
					  <li> PERSONAL ABUSE  </li> \
						<li>  QA DISCUSSIONS  </li>\
						 <li> RIGHT TO POST  </li> \
						 <li>CONTENT OWNERSHIP </li> \
					  </ul>  <br> \
					   ==================================================================================<br>\
				. Which one would you like to know about ?");
			}

		  else if (((message.toLowerCase().indexOf("i")<=0)||(message.toLowerCase().indexOf("what")<=0))&&((message.toLowerCase().indexOf("know")>=0)&& message.toLowerCase().indexOf("sololearn")>=0))
			{
			send_message("what about sololearn ?");
			 }
			 
		  else if (message.toLowerCase().indexOf("anything")>=0 )
			 {
			send_message ("Would you be more specific ?");
			 }

		  else if ((message.toLowerCase().indexOf("content creation")>=0)&&(message.toLowerCase().indexOf("personal abuse")>=0)){
			send_message("One at a time please . Ask me about Content creation or Personal abuse , not both . I can't handle that much load .")
			}

		  else if ((message.toLowerCase().indexOf("content creation")>=0)&&(message.toLowerCase().indexOf("qa discussions")>=0)){
			send_message("One at a time please . Ask me about Content creation or qa discussions, not both . I can't handle that much load .")
			}
		  else if ((message.toLowerCase().indexOf("content creation")>=0)&&(message.toLowerCase().indexOf("right to post")>=0)){
			send_message("One at a time please . Ask me about Content creation or Right to Post, not both . I can't handle that much load .")
		   }
		  else if ((message.toLowerCase().indexOf("content creation")>=0)&&(message.toLowerCase().indexOf("content ownership")>=0)){
			send_message("One at a time please . Ask me about content creation or Content Ownership , not both . I can't handle that much load .")
		  }
		  else if ((message.toLowerCase().indexOf("personal abuse")>=0)&&(message.toLowerCase().indexOf("qa discussions")>=0)){
			send_message("One at a time please . Ask me about Personal abuse or Qa discussions , not both . I can't handle that much load .")
		  }
		  else if ((message.toLowerCase().indexOf("personal abuse")>=0)&&(message.toLowerCase().indexOf("right to post ")>=0)){
			send_message("One at a time please . Ask me about  Personal abuse or Right to Post , not both . I can't handle that much load .")
		  }
		  else if ((message.toLowerCase().indexOf("personal abuse")>=0)&&(message.toLowerCase().indexOf("content ownership")>=0)){
		    send_message("One at a time please . Ask me about Personal abuse or Content ownership , not both . I can't handle that much load .")
	      }
	      else if ((message.toLowerCase().indexOf("qa discussions")>=0)&&(message.toLowerCase().indexOf("right to post ")>=0)){
		    send_message("One at a time please . Ask me about Qa discussions or Right to post , not both . I can't handle that much load .")
	      }
	      else if ((message.toLowerCase().indexOf("qa discussions")>=0)&&(message.toLowerCase().indexOf("content ownership")>=0)){
		    send_message("One at a time please . Ask me about Qa discussions or Content ownership , not both . I can't handle that much load .")
	      }
	      else if ((message.toLowerCase().indexOf("right to post")>=0)&&(message.toLowerCase().indexOf("content ownership")>=0)){
		    send_message("One at a time please . Ask me about Right to post or Content ownership , not both . I can't handle that much load .")
	      }
	

		  else if (message.toLowerCase().indexOf("content creation")>=0){
		    send_message("Posts by <span style='color:rgb(50, 230, 59);font-weight:bolder;'>SoloLearn </span> community members \
				 should be : <ul> <li>  Programming-related</li> <li> Aimed at\
				  helping individual learners and community members improve their programming skills by creating a respectful resource base </li>.\
				  <li> Posts may also focus on improving aspects of the platform and providing \
				  the community with improved content, whenever applicable.</li> ")
			 }

		  else if (message.toLowerCase().indexOf("personal abuse")>=0){
			send_message(" <ul> <li>  Personal attacks or disparagement of other users or their content is not tolerated.</li> \
				 <li> Every community member should be respectful and considerate, and assume that other people are also trying\
				  to make SoloLearn a great development resource.</li>\
				   <li> This means respecting opposing or differing opinions, beliefs, and conclusions; making an effort to\
				  listen to and understand others with whom you may disagree </li> ")
			 }

		  else if (message.toLowerCase().indexOf("qa discussions")>=0){
			send_message("<ul> <li>After adding a post, the original poster has a grace period during which he \
				 or she is permitted to delete the post</li>\
				 </ul> The Questions containing the following will be deleted :<br> \
				 \
				 <ul> <li> Content is created with the purpose of attracting spam content. </li> \
				 <li> Posts that are incoherent or otherwise impossible to answer meaningfully, and would not be improved by straightforward edits </li>.\
				 <li>Posts that focus on the promotion of a product or service</li>.\
				<li>  Posts that include inappropriate language, content, or reference.</li>\
				</ul>");
			 }

		  else if (message.toLowerCase().indexOf("content ownership")>=0){
			send_message(" <ul> <li>  You retain ownership of and responsibility for the content you create </li> \
				 <li> Not just  limited to, codes, posts, quizzes, and lessons. You also allow us certain\
				 rights that enable us to display and share your posted content.</li> <li> You retain control over your \
				 content, and you are responsible for it</li> </ul> ");
			 }

		  else if (message.toLowerCase().indexOf("right to post")>=0){
			send_message("<ul>  \
				 <li> We have the right to remove content or close accounts, if necessary. </li> \
				\
				\
				 <li> If youre posting anything you did not create yourself, you agree that you will only submit content that you\
				  have the right to post, and you will fully comply with any third-party licenses relating to content you post.</li> \
				 \
				 <li> If you are a copyright owner, and you believe that your rights have been violated, \
				 please contact us by emailing <span style='color:rgb(50, 230, 59);font-weight:bold;'> info@sololearn.com.</span> </ul> ");
			 }

		  else if (message.toLowerCase().indexOf("bye")>=0){
			send_message("Good Bye . Have a Wonderful time ");
				 $("#container_").delay(2000).fadeOut();
				 $("#container_").html(" ");
				 $("#container_").fadeIn();
;			 }

		  else{
			send_message("You can ask me Questions like  'what do you know about sololearn '  or  'what can you tell me about sololearn' etc etc  ");
			 }

			}
			
		  
$("document").ready(function(){

	get_username();

	//send text by clicking enter 

	$("#textBox").keypress(function(event){
		if( event.which == 13){
			if($("#checkbox").prop("checked")){
				$("#send").click();
				// runs the same code as if user were to click the send button 

				event.preventDefault();
		
			}
		}
	});

$("#send").click(function(){

	var userName = " <span class = 'userName'> You </span> ";

	var txt = $("#textBox").val();
	$("#textBox").val(" ");
	 
	var prevMsg = $("#container_").html();

	$("#container_").html(prevMsg + userName + ": " + txt + "<br>"  );

	//For getiing the messages to scroll up top .
	$("#container_").scrollTop($("#container_").prop("scrollHeight"));

	ai(txt);
     });
       
});







