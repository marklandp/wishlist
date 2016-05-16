 $(window).load(function() {
  $(".close").click(dismiss);
  $(".choose").click(accept);
  $("#showbought").click(toggle);
  $(".fancy").fancybox({
  		scrolling:'no',
  		openEffect	: 'elastic',
  		closeEffect	: 'elastic'
   });
  $("#fancyprocess").fancybox({
    type: 'inline',
    title: '<h4>Click on an Image to select it as your wish thumbnail.</h4>',
  		scrolling:'yes',
  		autoSize : false,
    width    : "82%",
    height   : "auto",
  		openEffect	: 'elastic',
  		closeEffect	: 'elastic',
  		closeClick: true
   }).trigger("click");
  $( "#updateView" ).submit(function(event){
    var cat = $("#category").val();
    event.preventDefault();
    var rxml = $.ajax({
        url: "/api/user/update-view",
        type: "POST",
        data: {
            category:cat
        }
    })
      .done(function () {
        var result = rxml.responseText;
        $("#wishes").html(result);
        }
      );
  });
$(".entry").click(delWish);
$(".entry2").click(bought);
 });
 
 function dismiss() {
  $(".alert-dismissable").hide("slow");
 }
  
 function accept(event) {
  var source = event.target.src;
  $("#thumbnail").attr("src",source);
  $("#thumb").attr('value',source);
 }
 
function toggle() {
 $(".needed").toggle("slow");
 $(".bought").toggle("slow");
}

function delWish(event) {
  var entry = $('.entry');
  if (entry.is(':checked')) {
   var sure = confirm("Do you really want to delete your wish?");
   if (sure == true) {
    var wish = $(event.target).val();
    var url = "/api/wish/"+wish+"/delete";
    $(location).attr("href", url);
   }
  }
 }
 
 function bought(event) {
  var entry = $('.entry2');
  if (entry.is(':checked')) {
   var sure = confirm("Confirm mark item as bought?");
   if (sure == true) {
    var wish = $(event.target).val();
    var url = "/api/wish/"+wish+"/bought";
    $(location).attr("href", url);
   }
  }
 }