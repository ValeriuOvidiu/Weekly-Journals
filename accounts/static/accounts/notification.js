window.onload = unreadNotification()

function unreadNotification() {
    $.ajax({
        method: "GET",
        url: "/unread_notification",
        success: function (data) {
            const messageInputDom = document.querySelector('#notif');
            if (data.unread_notf != 0) {
                messageInputDom.innerText = data.unread_notf;
            }
        },
        error: function (error) {
            getFriendshipStatus()
        }
    })
    render_friend_requests()
}

function render_friend_requests() {
    try {
        const displayNotification = document.getElementById("friend_requests")
        let numberOfNotification = friendRequest.length
        console.log(friendRequest, numberOfNotification)
        for (let i = 0; i < numberOfNotification; ++i) {
            let listItem = document.createElement("div");
            if (i < unreadFriendRequests) {
                if (friendRequest[i].sender_username != username) {
                    listItem.innerHTML = "<li  class=\"list-group-item list-group-item-dark\"> " +
                        "<p><a href=\"/other_user_profile/" + friendRequest[i].sender_username + "/hours-worked\"  class=\"black_links\"> <p class=\"unread\">" + friendRequest[i].sender_first_name + " " + friendRequest[i].sender_last_name + "</p></a> send you a friend request!" + "</p><button class=\"accept-button\" id=\"acceptButton" + i + "\">Accept</button><button class=\"delete-button\" id=\"deleteButton" + i + "\">Delete</button>" +
                        "<p class=\"date\">" + friendRequest[i].date + "</p>"
                    "</li>"
                    displayNotification.appendChild(listItem);
                } else {
                    listItem.innerHTML = "<li  class=\"list-group-item list-group-item-dark\"> " +
                        "<p><a href=\"/other_user_profile/" + friendRequest[i].receiver_username + "/hours-worked\"  class=\"black_links\"> <p class=\"unread\">" + friendRequest[i].receiver_first_name + " " + friendRequest[i].receiver_last_name + "</p></a> accepted Your friend request!" + "</p>" +
                        "<p class=\"date\">" + friendRequest[i].date + "</p>"
                    "</li>"
                    displayNotification.appendChild(listItem);
                }
            }
            else {
                listItem.innerHTML = "<li  class=\"list-group-item list-group-item-light\"> " +
                    "<p><a href=\"/other_user_profile/" + friendRequest[i].sender_username + "/hours-worked\"  class=\"black_links\"> <p class=\"unread\">" + friendRequest[i].sender_first_name + " " + friendRequest[i].sender_last_name + "</p></a> send you a friend request!!" + "</p><button class=\"accept-button\" id=\"acceptButton" + i + "\">Accept</button><button class=\"delete-button\" id=\"deleteButton" + i + "\">Delete</button> " +
                    "<p class=\"date\">" + friendRequest[i].date + "</p>"
                "</li>"
                displayNotification.appendChild(listItem);
            }
            let acceptButton = document.getElementById("acceptButton" + i)
            acceptButton.addEventListener("click", function () { acceptFriendRequestFromList(friendRequest[i], listItem) })

            let deleteButton = document.getElementById("deleteButton" + i)
            deleteButton.addEventListener("click", function () { delteFriendRequest(friendRequest[i], listItem) })
        }

    } catch {
        console.log('this is not notification page')
    }

}



function acceptFriendRequestFromList(sender, listItem) {

    console.log('acceptfunction')
    $.ajax({
        method: "GET",
        url: "/friend_request_handler/" + sender.sender_username,

        success: function (data) {
            listItem.innerHTML = "<li  class=\"list-group-item list-group-item-dark\"> " +
                "<p><a href=\"/other_user_profile/" + sender.sender_username + "/hours-worked\"  class=\"black_links\"> <p class=\"unread\">" + sender.sender_first_name + " " + sender.sender_last_name + "</p></a> send you a friend request!" + "</p><button class=\"disabled-button\" id=\"acceptButton\" disabled>Friend Request Accepted</button>" +
                "<p class=\"date\">" + sender.date + "</p>"
            "</li>"

            const chatSocket = new WebSocket(endpointWs + sender.sender_id);
            chatSocket.onclose = function (e) {
                console.log('close');
            };
            const notification = document.querySelector('#notif');
            const message = notification.value;
            chatSocket.onopen = () => chatSocket.send(JSON.stringify({
                'username': sender.sender_username
            }));
            notification.value = ''
        },
        error: function (error) {
            location.href=location.href
            
        }
        
    })
}

function delteFriendRequest(sender, listItem) {
    $.ajax({
        method: "GET",
        url: "/send_friend_requeast/" + sender.sender_username,
        success: function (data) {
            listItem.innerHTML = "<li  class=\"list-group-item list-group-item-dark\"> " +
                "<p><a href=\"/other_user_profile/" + sender.sender_username + "/hours-worked\"  class=\"black_links\"> <p class=\"unread\">" + sender.sender_first_name + " " + sender.sender_last_name + "</p></a> send you a friend request!" + "</p><button class=\"disabled-button\" id=\"acceptButton\" disabled>Friend Request Deleted</button>" +
                "<p class=\"date\">" + sender.date + "</p>"
            "</li>"
            const chatSocket = new WebSocket(endpointWs, sender.sender_id);
            chatSocket.onclose = function (e) {
            };
            const notification = document.querySelector('#notif');
            const message = notification.value;
            chatSocket.onopen = () => chatSocket.send(JSON.stringify({
                'username': sender.username
            }));
            notification.value = ''
        },
        error: function (error) {

        }
    })
}
