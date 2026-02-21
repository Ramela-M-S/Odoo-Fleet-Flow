document.addEventListener("DOMContentLoaded", () => {

const drivers = [
  { name:"Alex", expiry:"2026-12-31", completion:92, safety:88, status:"On Duty" },
  { name:"Maria", expiry:"2024-03-01", completion:75, safety:70, status:"Off Duty" },
  { name:"John", expiry:"2023-01-10", completion:60, safety:55, status:"Suspended" }
];

const tbody = document.getElementById("driverTableBody");

drivers.forEach(d => {

  const expired = new Date(d.expiry) < new Date();

  const row = document.createElement("tr");

  row.innerHTML = `
    <td><strong>${d.name}</strong></td>
    <td>
      ${d.expiry}
      ${expired ? '<span class="badge expired-badge ms-2">Expired</span>' : ''}
    </td>
    <td>
      <div class="progress">
        <div class="progress-bar" style="width:${d.completion}%">
          ${d.completion}%
        </div>
      </div>
    </td>
    <td>
      <span class="badge ${d.safety > 75 ? 'bg-success' : 'bg-warning'}">
        ${d.safety}
      </span>
    </td>
    <td>
      <select class="form-select status-select">
        <option ${d.status=="On Duty"?"selected":""}>On Duty</option>
        <option ${d.status=="Off Duty"?"selected":""}>Off Duty</option>
        <option ${d.status=="Suspended"?"selected":""}>Suspended</option>
      </select>
    </td>
  `;

  tbody.appendChild(row);
});

});