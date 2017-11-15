 $(document).ready(function(){
        
        if($("#username").is(":focus"))
        {
          console.log("focus");
          $("#warning").addClass("invisible");
        }

        $(".result").click(function(){
          

          var username= $("#username").val();
          console.log(username);


          if(!username)
          {
             $("#warning").removeClass("invisible");
          }

          else{

            console.log("else mein aa gaya");
            $("#warning").addClass("invisible");
            $(".result").attr("href", "#about");
            $(".result").addClass("js-scroll-trigger");
            $("#search").addClass("fa-spinner fa-spin");
            //call a script here to find the username

           /* setTimeout(
            function() 
            {
              //call script here

              $("#search").removeClass("fa-spinner fa-spin fa-exclamation-triangle");
            }, 1000);
          */
            re  = callpy(username);
            console.log(username + " Fuck"+re);

            $("#search").addClass("fa-check");

            $("#data").addClass("fa-spinner fa-spin");
            //call a script here to collect data
            setTimeout(
            function() 
            {
              //call script here
              $("#data").removeClass("fa-spinner fa-spin fa-exclamation-triangle");
            }, 2000);
          
            $("#data").addClass("fa-check");

            $("#climax").addClass("fa-spinner fa-spin");
            $("#climax").removeClass("animated");
            //call a script here to find the username
            setTimeout(
            function() 
            {
              //call script here
              $("#climax").removeClass("fa-spinner fa-spin fa-exclamation-triangle animated");
            }, 3000);
          
            $("#climax").addClass("fa-check");

            $("#script-result").addClass("fa-spinner fa-spin");
            $("#script-result").removeClass("animated");
            //call a script here to find the username
            setTimeout(
            function() 
            {
              //call script here
              $("#script-result").removeClass("fa-spinner fa-spin fa-exclamation-triangle");
              $("#script-result").addClass("fa-chevron-down animated faa-falling");
            }, 4000);
          
          }

        });

      });


 function callpy(username)
 {
  var temp = {
    'username' : username
  }
  console.log("callpy mein hun");
    $.ajax({
      type: "POST",
      url: "http://13.58.87.15:8000/getUser",
      dataType: 'json',
      data: JSON.stringify(temp),
      xhrFields: {
       withCredentials: true
      },
      
    }
    }).done(function(result){
      console.log();
    });
      return response;
 }