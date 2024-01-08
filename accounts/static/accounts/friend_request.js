function sendFriendRequest() {
    console.log("alea")

    $.ajax({
        method: "GET",
        url: "/send_friend_requeast/" + username,
        success: function (data) {
            getFriendshipStatus()  
            const notification = document.querySelector('#notif');
            const message = notification.value;
            chatSocket.send(JSON.stringify({
                'username': username
            }));
            notification.value = ''
        },
        error: function (error) {
            getFriendshipStatus()
        }
    })

}

let showDeleteFriendButton=true
function getFriendshipStatus() {
    let friendRequestDiv = document.getElementById("friendRequest")
console.log('mesaj din getfriendshipStatus')
    $.ajax({
        method: "GET",
        url: "/get_friendship_status/" + username,

        success: function (data) {
            console.log(data.friendship_status)
            friendRequestDiv.innerHTML = ""
            if (data.friendship_status == "Cancel the friend request") {
                let cancelButton = document.createElement("button")
                cancelButton.addEventListener("click", sendFriendRequest)
                cancelButton.classList.add("delete-button")
                cancelButton.innerText = data.friendship_status
                friendRequestDiv.appendChild(cancelButton)
            } else if (data.friendship_status == "Accept") {
                let acceptButton = document.createElement("button")
                acceptButton.classList.add("accept-button")
                acceptButton.addEventListener("click",acceptFriendRequest)
                acceptButton.innerText = data.friendship_status
                friendRequestDiv.appendChild(acceptButton)
                let cancelButton = document.createElement("button")
                cancelButton.addEventListener("click", sendFriendRequest)
                cancelButton.classList.add("delete-button")
                cancelButton.innerText = "Delete"
                friendRequestDiv.appendChild(cancelButton)
            } else if (data.friendship_status == "Add") {
                let acceptButton = document.createElement("button")
                acceptButton.addEventListener("click", sendFriendRequest)
                acceptButton.classList.add("accept-button")
                acceptButton.innerHTML=feather.icons['user-plus'].toSvg();

                acceptButton.innerHTML += data.friendship_status
                friendRequestDiv.appendChild(acceptButton)
            } else {
                console.log("intra")
                let friendButton = document.createElement("button")  
               friendButton.classList.add("friends_button")
                friendButton.innerHTML=feather.icons['user-check'].toSvg();
                friendButton.innerHTML+="Friends"
                friendButton.addEventListener("click",function(e){
                    friendRequestDiv.innerHTML = ""
                    if (showDeleteFriendButton){
                    let deleteFriendButton=document.createElement("a")
                    deleteFriendButton.innerHTML+="<button id=\"delete\" class=\"delete_friend_button\"> </buttton>"  
                    deleteFriendButton.href="/friend_request_handler/" + username
                    friendRequestDiv.appendChild(document.createElement("b"))
                    friendRequestDiv.appendChild(friendButton)
                    friendRequestDiv.appendChild(deleteFriendButton)
                    document.getElementById("delete").innerHTML=feather.icons['user-x'].toSvg()
                    document.getElementById("delete").innerHTML+="Delete"
                    showDeleteFriendButton=false 
                    }
                    else{
                        friendRequestDiv.appendChild(friendButton)
                        showDeleteFriendButton=true 
                    }
                })

                friendRequestDiv.appendChild(friendButton) 
                feather.replace();
            }


            console.log(data)

        },
        error: function (error) {
            friendRequestDiv.innerText = "alealalte"
        }

    })
}
window.onload = getFriendshipStatus()

function acceptFriendRequest() {
    $.ajax({
        method: "GET",
        url: "/friend_request_handler/" + username,

        success: function (data) {
            getFriendshipStatus()
            location.href = location.href;
            const notification = document.querySelector('#notif');
                    const message = notification.value;
                    chatSocket.send(JSON.stringify({  
                        'username': username
                    }));
                    notification.value = ''
        },
        error: function (error) {
            getFriendshipStatus()
        }

    })
}


 

 