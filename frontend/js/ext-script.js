
window.onload = function() {
  $('.card').css("cursor", "pointer");

  $("#tab-contenuto").load("datiaggregati.html", function () {
    $('.card').hover(function(){
          $(this).addClass('transition');
    },function(){
        $(this).removeClass('transition');
    });
    $('#citySelect').on('change', function() {
        citta =  $(this).find(":selected").val();


        $(".scarica-eventi").click(function() {
          window.open("download.php?citta="+ citta + "&tipologia=Eventi")
        });
        $(".scarica-verdi").click(function() {
          window.open("download.php?citta="+ citta + "&tipologia=AreeVerdi")
        });


        $(".card").fadeOut( 600, "linear" );
        $(".card").fadeIn( 600, "linear" );
    });
  });

  $("#btn-singolo").on('click', function(){
    $("#tab-contenuto").fadeOut(800, function() {
      $("#tab-contenuto").load("daticomune.html", function () {
        $('.card').hover(function(){
              $(this).addClass('transition');
        },function(){
            $(this).removeClass('transition');
        });
        $('#citySelect').on('change', function() {
            citta =  $(this).find(":selected").val();


            $(".scarica-eventi").click(function() {
              window.open("download.php?citta="+ citta + "&tipologia=Eventi", "_self")
            });
            $(".scarica-verdi").click(function() {
              window.open("download.php?citta="+ citta + "&tipologia=AreeVerdi", "_self")
            });

            $(".card").fadeOut( 600, "linear" );
            $(".card").fadeIn( 600, "linear" );
        });
      });
      $('#citySelect').on('change', function() {
          citta =  $(this).find(":selected").val();


          $(".scarica-eventi").click(function() {
            window.open("download.php?citta="+ citta + "&tipologia=Eventi", "_self")
          });
          $(".scarica-verdi").click(function() {
            window.open("download.php?citta="+ citta + "&tipologia=Verdi", "_self")
          });


          $(".card").fadeOut( 600, "linear" );
          $(".card").fadeIn( 600, "linear" );
      });

    })
    $("#tab-contenuto").fadeIn(400, function() {
      //Stuff to do *after* the animation takes place
    });
  });


  $("#btn-aggr").on('click', function(){
    $("#tab-contenuto").fadeOut(800, function() {
      $("#tab-contenuto").load("datiaggregati.html", function () {
        $('.card').hover(function(){
              $(this).addClass('transition');
        },function(){
            $(this).removeClass('transition');
        });

      });
      $("#tab-contenuto").fadeIn(400, function() {
        //Stuff to do *after* the animation takes place
      })
    })

  });

};

// anche tornando indietro funziona
window.addEventListener("pageshow", function() {
  $("#citySelect").val("");
  clearHref()
}, false);

$(".tour").on('click', function(){
  console.log("ciao");
  introJs().start();
})

function clearHref(){
  $(".scarica-eventi").attr("href","#");
  $(".scarica-offerta").attr("href","#");
  $(".scarica-fontanelle").attr("href","#");
  $(".scarica-verdi").attr("href","#");
  $(".scarica-parcheggi").attr("href","#");

}
