
let apiData="test"
$.ajax({      
 method: "GET",
 url :'/charts/get_data_for_sleep_chart/'+username+'/'+date ,  
 success: function(data){  

let daily_charts_data=data[0]
let week_charts_data=data[1]
console.log(data)
const ctx = document.getElementById('dailyChart');
const secondctx=document.getElementById('weekleyChart')  

new Chart(ctx, {
type: 'line',
data: {
labels: daily_charts_data[0], // Aici pui etichetele pentru axa X (zilele)
datasets: [{
 label: 'Hours Slept',
 data: daily_charts_data[1],
 borderColor: 'rgba(75, 192, 192, 1)', // Culoarea liniei graficului
 fill: false // Dacă dorești să umpli zona sub grafic sau nu
},]
},
options: {

}
});
new Chart(secondctx, {
type: 'line',
data: {
labels: week_charts_data[0], // Aici pui etichetele pentru axa X (zilele)
datasets: [{
 label: 'Hours Slept',  
 data: week_charts_data[1],
 borderColor: 'rgba(75, 192, 192, 1)', // Culoarea liniei graficului
 fill: false // Dacă dorești să umpli zona sub grafic sau nu
},]
},
options: {

}
});
 },
 error:function(error){   
   console.log(error)  
   console.log("eeroereeee")
 }

}) 