function openImage(imageUrl) {
    var modal = document.getElementById('imageModal');
    
    var modalImg = document.getElementById('fullSizeImage');
    modalImg.src = imageUrl;
    modal.style.display = 'block';
  
    var span = document.getElementsByClassName('close')[0];
    span.onclick = function() { 
      modal.style.display = 'none';
    }
    window.onclick = function(event) {
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    }
  }