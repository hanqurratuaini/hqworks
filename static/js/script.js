document.getElementById('mom-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const title = document.getElementById('title').value;
  const date = document.getElementById('date').value;
  const attendees = document.getElementById('attendees').value.split("\n").map(item => {
    const [group, members] = item.split("|");
    return { group_name: group.trim(), members: members.trim() };
  });
  const notes = document.getElementById('notes').value;

  fetch('/generate_mom', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: title,
      date: date,
      attendees: attendees,
      notes: notes
    })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('mom-output').innerText = `Generated MoM:\n\n${data.mom}`;
  })
  .catch(error => console.error('Error:', error));
});
