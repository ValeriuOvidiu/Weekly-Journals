
let apiData="test"
$.ajax({      
 method: "GET",
 url :'/charts/get_data_for_sleep_chart/'+username+'/'+date ,  
 success: function(data){  

let dailyChartsData=data[0]
let weekChartsData=data[1]
console.log(data)
const ctx = document.getElementById('dailyChart');
const secondctx=document.getElementById('weekleyChart')  

new Chart(ctx, {
type: 'line',
data: {
labels: dailyChartsData[0], // Aici pui etichetele pentru axa X (zilele)
datasets: [{
 label: 'Hours Slept',
 data: dailyChartsData[1],
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
labels: weekChartsData[0], // Aici pui etichetele pentru axa X (zilele)
datasets: [{
 label: 'Hours Slept',  
 data: weekChartsData[1],
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