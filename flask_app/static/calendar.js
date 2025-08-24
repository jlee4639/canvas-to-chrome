/* Hold all events from fullcalendar */
const fullcalendar_events = []

/* Import FullCalendar.io */
document.addEventListener('DOMContentLoaded', function() {
    /* Extract canvas_assignment data */
    const assignments_with_dates = document.getElementById("assignments_dated");
    const assignments_without_dates = document.getElementById("assignments_undated");
    let canvas_events = [];

    /* Extract events with dates */
    if (assignments_with_dates){
        canvas_events = JSON.parse(assignments_with_dates.dataset.info);
    }

    /* Add assignments_with_dates data to fullcalendar_events */
    fullcalendar_events.push(...canvas_events)

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        aspectRatio: 1.7,
        editable: true,
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
            node.style.borderColor = color;
            node.style.borderStyle = "solid";
            node.style.borderWidth = "2px";
            node.style.borderRadius = "5px"

            /* Set event text */
            node.innerText = `${formatted_time} - ${arg.event.title}`;

            return {domNodes: [node]};
        },
        /* Make sure to change the comments to make calendar eents appear */
         events: canvas_events
        /*events: [{start:"2025-08-15T00:00:00", end:"2025-08-15T23:59:59", title:"Test Event"}]*/
    });

    calendar.render();

    /* Send fullcalendar events to calendar_events hidden field*/
    const export_form = document.querySelector("form");
    console.log(export_form)

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
});