const nextButton = document.querySelector(".right-arrow");
const previousButton = document.querySelector(".left-arrow");

const leftPage = document.getElementById("left-page");
const rightPage = document.getElementById("right-page");

const tripData = document.getElementById("trip-data");

const destination = tripData.dataset.destination;
const days = tripData.dataset.days;
const travellers = tripData.dataset.travellers;
const budget = tripData.dataset.budget;

let currentSpread = 0;

const spreads = [
  {
    left: `
      <h2>Enjoy Your Customised Trip</h2>
      <p>Your journey has been shaped around the way you like to travel.</p>

      <div class="notebook-note">
        <p><strong>Destination:</strong> ${destination}</p>
        <p><strong>Travellers:</strong> ${travellers}</p>
        <p><strong>Duration:</strong> ${days} days</p>
        <p><strong>Budget:</strong> ₹${budget}</p>
      </div>
    `,

    right: `
      <h2>Day 1</h2>
      <p class="day-subtitle">Arrival & Local Exploration</p>

      <div class="day-section">
        <h3>Morning</h3>
        <p>Arrive at your destination and settle in.</p>
      </div>

      <div class="day-section">
        <h3>Afternoon</h3>
        <p>Explore a nearby local attraction.</p>
      </div>

      <div class="day-section">
        <h3>Evening</h3>
        <p>Discover local food and explore the surroundings.</p>
      </div>
    `,
  },

  {
    left: `
      <h2>Day 1</h2>
      <p class="day-subtitle">Arrival & Local Exploration</p>

      <div class="day-section">
        <h3>Morning</h3>
        <p>Arrive at your destination and settle in.</p>
      </div>

      <div class="day-section">
        <h3>Afternoon</h3>
        <p>Explore a nearby local attraction.</p>
      </div>

      <div class="day-section">
        <h3>Evening</h3>
        <p>Discover local food and explore the surroundings.</p>
      </div>
    `,

    right: `
      <h2>Day 2</h2>
      <p class="day-subtitle">Discover Something New</p>

      <div class="day-section">
        <h3>Morning</h3>
        <p>Explore a new destination or experience.</p>
      </div>

      <div class="day-section">
        <h3>Afternoon</h3>
        <p>Enjoy a local activity.</p>
      </div>

      <div class="day-section">
        <h3>Evening</h3>
        <p>Relax and explore the local surroundings.</p>
      </div>
    `,
  },

  {
    left: `
      <h2>Day 2</h2>
      <p class="day-subtitle">Discover Something New</p>

      <div class="day-section">
        <h3>Morning</h3>
        <p>Explore a new destination or experience.</p>
      </div>

      <div class="day-section">
        <h3>Afternoon</h3>
        <p>Enjoy a local activity.</p>
      </div>

      <div class="day-section">
        <h3>Evening</h3>
        <p>Relax and explore the local surroundings.</p>
      </div>
    `,

    right: `
      <h2>Day 3</h2>
      <p class="day-subtitle">Local Experiences</p>

      <div class="day-section">
        <h3>Morning</h3>
        <p>Discover a local experience.</p>
      </div>

      <div class="day-section">
        <h3>Afternoon</h3>
        <p>Visit another interesting spot.</p>
      </div>

      <div class="day-section">
        <h3>Evening</h3>
        <p>Enjoy your final evening.</p>
      </div>
    `,
  },
];

function showSpread() {
  leftPage.innerHTML = spreads[currentSpread].left;
  rightPage.innerHTML = spreads[currentSpread].right;
}

nextButton.addEventListener("click", function () {
  if (currentSpread < spreads.length - 1) {
    currentSpread++;
    showSpread();
  }
});

previousButton.addEventListener("click", function () {
  if (currentSpread > 0) {
    currentSpread--;
    showSpread();
  }
});

showSpread();
