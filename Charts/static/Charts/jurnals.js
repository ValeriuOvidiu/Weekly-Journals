const endpoint = '/jurnals_data/' + username + '/' + date
let apiData = "test"
const monthsOfYear = [
  { name: 'January', number: '01' },
  { name: 'February', number: '02' },
  { name: 'March', number: '03' },
  { name: 'April', number: '04' },
  { name: 'May', number: '05' },
  { name: 'June', number: '06' },
  { name: 'July', number: '07' },
  { name: 'August', number: '08' },
  { name: 'September', number: '09' },
  { name: 'October', number: '10' },
  { name: 'November', number: '11' },
  { name: 'December', number: '12' }
];
function getMonthNameByNumber(monthNumber) {
  for (let i = 0; i < monthsOfYear.length; i++) {
    if (monthsOfYear[i].number === monthNumber) {
      return monthsOfYear[i].name;
    }
  }
  return 'Luna nu a fost găsită';
}
$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {

    let daily_worked_data = data[0]
    let week_slept_data = data[1]
    console.log(data, "ceva")
    const ctx = document.getElementById('dailyChart');
    const secondctx = document.getElementById('weekleyChart')
    const week = document.getElementById('week')
    const weekTotalWork=document.getElementById('weekTotalWork')
    const weekTotalSleep=document.getElementById('weekTotalSleep')
    let weekTotalWork2=0
    let weekTotalSleep2=0
    for(let i=0;i<7;++i){
      weekTotalWork2+=daily_worked_data[1][i]
      weekTotalSleep2+=week_slept_data[1][i]
    }
    weekTotalWork.innerHTML= "Week total worked hours = "+weekTotalWork2  
    weekTotalSleep.innerHTML= "Week total slept hours = "+weekTotalSleep2 

    let endDate = daily_worked_data[0][6]
    let beginingDate = daily_worked_data[0][0]
    if (beginingDate.substring(5, 7) != daily_worked_data[0][6].substring(5, 7)) {
      week.innerHTML = "This is the week " + beginingDate.substring(8) + " " + getMonthNameByNumber(beginingDate.substring(5, 7)) + '-' + endDate.substring(8) + " "+getMonthNameByNumber(endDate.substring(5, 7))
    }else{
      week.innerHTML="This is the week " + beginingDate.substring(8) +  '-' + endDate.substring(8) + " "+getMonthNameByNumber(endDate.substring(5, 7))
    }
    
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: daily_worked_data[0], // Aici pui etichetele pentru axa X (zilele)
        datasets: [{
          label: 'Hours Worked',
          data: daily_worked_data[1],
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
        labels: week_slept_data[0], // Aici pui etichetele pentru axa X (zilele)
        datasets: [{
          label: 'Hours Slept',
          data: week_slept_data[1],
          borderColor: 'rgba(75, 192, 192, 1)', // Culoarea liniei graficului
          fill: false // Dacă dorești să umpli zona sub grafic sau nu
        },]
      },
      options: {

      }
    });
  },
  error: function (error) {
    console.log(error)
    console.log("eeroereeee")
  }

}) 