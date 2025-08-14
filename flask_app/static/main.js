/* Import FullCalendar.io */
document.addEventListener('DOMContentLoaded', function() {
    /* Extract canvas_assignment data */
    const canvas_assignments = document.getElementById("canvas_assignments");
    console.log(canvas_assignments);
    let canvas_events = [];

    if (canvas_assignments){
        canvas_events = JSON.parse(canvas_assignments.dataset.info);
    }

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: canvas_events
    });

    calendar.render();
});
