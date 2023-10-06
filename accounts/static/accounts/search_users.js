let searchField=document.getElementById("search")
searchField.addEventListener("keyup",getSugestions)
window.addEventListener("click",function(e){
  resultsList.innerHTML = "";     
})
searchField.addEventListener("click",getSugestions)
function getSugestions(){
    let searchFieldInput=searchField.value
    let endPoint="/search_users/"+searchFieldInput
    $.ajax({
        method: "GET",
        url: endPoint,
        success: function (data) {
            updateResultsList(data.results);
      console.log(data)
         
        },
        error: function (error) {
          updateResultsList([]);
        }
      
      }) 
}
let resultsList = document.getElementById("resultsList");
function updateResultsList(results) {
    resultsList.innerHTML = "";
  
    if (results.length === 0) {
      resultsList.style.display = "none";
      return;
    }
  
    resultsList.style.display = "block";
  
    results.forEach(function (result) {
      let listItem = document.createElement("a");
      console.log("asasas")
      listItem.href="/other_user_profile/"+result.username+"/hours-worked"  
      listItem.textContent = result.first_name +" "+result.last_name;
      console.log(result.first_name)
      listItem.classList.add("list-group-item"); 
      listItem.addEventListener("mouseover", function (e) {
        listItem.style.background="#e6e6e6"
      })    
      listItem.addEventListener("mouseout", function (e) {
        listItem.style.background="white"
      })  
     
      resultsList.appendChild(listItem);  
    });
  }
  
  
  
  
  
  