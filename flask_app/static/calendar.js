/* Hold all events from fullcalendar */
const fullcalendar_events = []
/* Hold data for modal event submission */
const modal_submission = [];

/* Event Colors */
const bgColors = ["#a4bdfc", "#7ae7bf", "#dbadff", "#ff887c", "#fbd75b", 
            "#ffb878", "#46d6db", "#A9A9A9", "#5484ed", "#51b749",
            "#dc2127"];

/* Add colors to radio events */
const button_cont = document.getElementById("color-buttons");

bgColors.forEach((color, index) => {
    const input_container = document.createElement("label");
    const radio_input = document.createElement("input");
    const radio_input_overlay = document.createElement("span");
    const hidden_input = document.createElement("input");

    /* Style radio button */
    radio_input.type = "radio";
    radio_input.name = "color";
    radio_input.value = color;
    radio_input.classList = "radio-button";
    radio_input.setAttribute("data-color-id", index);

    /* Style radio Button css */
    radio_input_overlay.classList = "color-radio-button";
    radio_input_overlay.style.backgroundColor = color;
    
    /* Add to container */
    input_container.appendChild(radio_input);
    input_container.appendChild(radio_input_overlay);
    button_cont.appendChild(input_container);
});


/* Import FullCalendar.io */
document.addEventListener('DOMContentLoaded', function() {
    /* Extract canvas_assignment data */
    const assignments_with_dates = document.getElementById("assignments_dated");
    const assignments_without_dates = document.getElementById("assignments_undated");
    let canvas_events = [];

    /* List all non-calendar events on the side tab */
    let uevent_list = document.getElementById("undated_event_list");
    let undated_events = [];

    /* Extract events without dates */
    if (assignments_without_dates){
        undated_events = JSON.parse(assignments_without_dates.dataset.info);
    }

    /* Add draggable events on the side */
    undated_events.forEach((event_data) => {
        /* Event container */
        const event_cont = document.createElement("div");

        /* Add class fullcalendar event to element */
        event_cont.classList.add("fc-event");

        /* Add css elements */
        const color = event_data.backgroundColor; 
        event_cont.innerText = event_data.title;
        event_cont.style.backgroundColor = "white";
        event_cont.style.border = "2px solid " + color;
        event_cont.style.borderRadius = "5px";
        event_cont.style.color = color;

        uevent_list.appendChild(event_cont);
    });

    /* Extract events with dates */
    if (assignments_with_dates){
        canvas_events = JSON.parse(assignments_with_dates.dataset.info);
    }

    /* Add assignments_with_dates data to fullcalendar_events */
    fullcalendar_events.push(...canvas_events)

    var calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        droppable: true,
        aspectRatio: 1.7,
        editable: true,
        selectable: true,
        initialView: 'dayGridMonth',  
        eventContent: function(arg) {
            /* Event node */
            const node = document.createElement("div");

            /* Set padding */
            node.style.padding = "3px";

            /* Format End time */
            let endTime = arg.event.end;
            let formatted_time = endTime.getHours().toString().padStart(2,'0') + ':' + 
                    endTime.getMinutes().toString().padStart(2,'0');

            /* Set background and border */
            const color = arg.event.backgroundColor;
            node.style.color = color;
            node.style.backgroundColor = "white";
            node.style.borderColor = color;
            node.style.borderStyle = "solid";
            node.style.borderWidth = "2px";
            node.style.borderRadius = "5px"

            /* Set event text */
            node.innerText = `${formatted_time} - ${arg.event.title}`;

            return {domNodes: [node]};
        },
        eventReceive: function(info) {
            console.log("Dropped event:", info.event);
        },
        dateClick: function(e){
            const modal = document.getElementById("event_modal");
            modal.dataset.date = e.dateStr;

            modal.showModal();


        },
         events: canvas_events
    });

    calendar.render();

    /* Send fullcalendar events to calendar_events hidden field*/
    const export_form = document.querySelector("#export_form");

    export_form.addEventListener("submit", (e) =>{
        const events = calendar.getEvents().map(event => ({
            summary: event.title,
            start: {
                dateTime: event.start
            },
            end: {
                dateTime: event.end
            },
            colorId: event.extendedProps.colorId
        }));

        const hidden_field = document.getElementById("fullcalendar_events");
        hidden_field.value = JSON.stringify(events)
    });

    /* Add modal form data as a calendar event */
    const modal_form = document.querySelector("#modal-form");
    const modal = document.querySelector("#event_modal");
    const hidden_input = document.querySelector("#hidden_color_id");

    /* Change form hidden input value every time radio button is changed */
    modal_form.addEventListener("change", (arg) => {
        if(arg.target.name == "color"){
            hidden_input.value = arg.target.dataset.colorId;
        }
    });

    /* Add calendar event after submitting modal form */
    modal_form.addEventListener('submit', (arg)=>{
        const formdata = new FormData(modal_form);  
        const date = modal.dataset.date;
        let timeStart = formdata.get('start-date');
        let timeEnd = formdata.get('end-date');

        /* Set the time to ISO8601 format */
        let startLocal = date + "T" + timeStart;
        let endLocal = date + "T" + timeEnd;

        console.log(`Title: ${formdata.get('title')}`);
        console.log(`Start Local: ${typeof(startLocal)}`);
        console.log(`End Local: ${timeEnd} + ${startLocal}`);
        console.log(`Start: ${new Date(startLocal).toISOString()}`);
        console.log(`Background: ${formdata.get("color")}`);
        console.log(`Color ID: ${formdata.get("hidden_color_id")}`);
        
        const event = {
            title: formdata.get('title'),
            start: new Date(startLocal).toISOString(),
            end: new Date(endLocal).toISOString(),
            backgroundColor: formdata.get("color"),
            extendedProps: {
                colorId: formdata.get("hidden_color_id")
            }
        }

        calendar.addEvent(event);

        modal.close();
    });
});