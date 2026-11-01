document.addEventListener("DOMContentLoaded", function () {
  // =========================================
  // 1. BUDGET PROGRESS BARS
  // =========================================

  document.querySelectorAll(".budget-fill[data-width]").forEach((fill) => {
    fill.style.width = `${fill.dataset.width}%`;
  });

  // =========================================
  // 2. THEME TOGGLE
  // =========================================

  const themeToggle = document.getElementById("theme-toggle");
  const html = document.documentElement;

  function setTheme(theme) {
    html.dataset.theme = theme;

    try {
      localStorage.setItem("waywise-theme", theme);
    } catch (error) {}

    const metaTheme = document.querySelector('meta[name="theme-color"]');

    if (metaTheme) {
      metaTheme.content = theme === "dark" ? "#171a20" : "#f5f7f8";
    }

    if (themeToggle) {
      themeToggle.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light mode" : "Switch to dark mode",
      );
    }
  }

  let savedTheme = "dark";

  try {
    savedTheme = localStorage.getItem("waywise-theme") || "dark";
  } catch (error) {}

  setTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const nextTheme = html.dataset.theme === "dark" ? "light" : "dark";

      setTheme(nextTheme);
    });
  }

  // =========================================
  // 3. MAKE IT CHEAPER
  // =========================================

  const savingOptions = document.querySelectorAll(".saving-option");
  const potentialSavings = document.getElementById("potential-savings");
  const revisedBudgetElement = document.getElementById("revised-budget");
  const applyButton = document.getElementById("apply-changes");
  const undoButton = document.getElementById("undo-changes");

  const tripData = document.getElementById("trip-data");

  let changesApplied = false;

  if (savingOptions.length && tripData) {
    const originalTotal = Number(tripData.dataset.budget) || 0;

    const originalCategories = {};

    document.querySelectorAll(".budget-category").forEach((category) => {
      const name = category
        .querySelector(".budget-category-heading span")
        ?.textContent.trim();

      const amountText =
        category.querySelector(".budget-category-heading strong")
          ?.textContent || "0";

      if (name) {
        originalCategories[name] =
          Number(amountText.replace(/[^\d.]/g, "")) || 0;
      }
    });

    function getSelectedAlternatives() {
      return Array.from(savingOptions).filter((option) => option.checked);
    }

    function getSavings() {
      return getSelectedAlternatives().reduce((total, option) => {
        return total + (Number(option.dataset.savings) || 0);
      }, 0);
    }

    function updateSavings() {
      const savings = getSavings();
      const revised = Math.max(0, originalTotal - savings);

      if (potentialSavings) {
        potentialSavings.textContent = `₹${Math.round(savings).toLocaleString("en-IN")}`;
      }

      if (revisedBudgetElement) {
        revisedBudgetElement.textContent = `₹${Math.round(revised).toLocaleString("en-IN")}`;
      }
    }

    function updateCategory(name, amount, total) {
      const category = Array.from(
        document.querySelectorAll(".budget-category"),
      ).find((item) => {
        return (
          item
            .querySelector(".budget-category-heading span")
            ?.textContent.trim() === name
        );
      });

      if (!category) return;

      const amountElement = category.querySelector(
        ".budget-category-heading strong",
      );

      const fill = category.querySelector(".budget-fill");

      if (amountElement) {
        amountElement.textContent = `₹${Math.round(amount).toLocaleString("en-IN")}`;
      }

      if (fill) {
        const percentage = total > 0 ? (amount / total) * 100 : 0;
        fill.style.width = `${percentage}%`;
      }
    }

    function getSelectedAccommodation() {
      const selected = getSelectedAlternatives().find((option) => {
        return option.dataset.category?.toLowerCase() === "accommodation";
      });

      if (!selected) return null;

      const name = selected.dataset.alternative.toLowerCase();

      if (name.includes("hostel")) return "hostel";
      if (
        name.includes("homestay") ||
        name.includes("guesthouse") ||
        name.includes("guest house")
      )
        return "homestay";
      if (name.includes("hotel")) return "hotel";

      return null;
    }

    async function updateStayRecommendations(accommodation) {
      const stayGrid = document.getElementById("stay-grid");

      if (!stayGrid || !accommodation) return;

      try {
        const destination = tripData.dataset.destination;

        const response = await fetch(
          `/get-stays?destination=${encodeURIComponent(destination)}&accommodation=${encodeURIComponent(accommodation)}`,
        );

        if (!response.ok) {
          throw new Error("Could not load stays.");
        }

        const result = await response.json();

        stayGrid.replaceChildren();

        if (!result.stays || !result.stays.length) {
          const message = document.createElement("p");
          message.textContent =
            "No stays match this accommodation preference yet.";
          stayGrid.appendChild(message);
          return;
        }

        result.stays.forEach((stay) => {
          const card = document.createElement("article");
          card.className = "recommendation-card";

          const tag = document.createElement("span");
          tag.className = "recommendation-tag";
          tag.textContent = stay.type || "";

          const heading = document.createElement("h3");
          heading.textContent = stay.name || "";

          const description = document.createElement("p");
          description.textContent = stay.best_for || "";

          const meta = document.createElement("div");
          meta.className = "recommendation-meta";

          const area = document.createElement("span");
          area.textContent = stay.area || "";
          meta.appendChild(area);

          const link = document.createElement("a");
          link.href = stay.url || "#";
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.textContent = "Explore stay ↗";

          card.append(tag, heading, description, meta, link);
          stayGrid.appendChild(card);
        });

        tripData.dataset.accommodation = accommodation;
      } catch (error) {
        console.error("Stay update error:", error);
      }
    }

    savingOptions.forEach((option) => {
      option.addEventListener("change", updateSavings);
    });

    if (applyButton) {
      applyButton.addEventListener("click", async function () {
        const savings = getSavings();
        const revised = Math.max(0, originalTotal - savings);

        const revisedCategories = { ...originalCategories };

        getSelectedAlternatives().forEach((option) => {
          const category = option.dataset.category;
          const saving = Number(option.dataset.savings) || 0;

          const matchingCategory = Object.keys(revisedCategories).find(
            (name) => name.toLowerCase() === category.toLowerCase(),
          );

          if (matchingCategory) {
            revisedCategories[matchingCategory] = Math.max(
              0,
              revisedCategories[matchingCategory] - saving,
            );
          }
        });

        Object.entries(revisedCategories).forEach(([name, amount]) => {
          updateCategory(name, amount, revised);
        });

        if (revisedBudgetElement) {
          revisedBudgetElement.textContent = `₹${Math.round(revised).toLocaleString("en-IN")}`;
        }

        const newAccommodation = getSelectedAccommodation();

        if (newAccommodation) {
          await updateStayRecommendations(newAccommodation);
        }

        changesApplied = true;
      });
    }

    if (undoButton) {
      undoButton.addEventListener("click", async function () {
        savingOptions.forEach((option) => {
          option.checked = false;
        });

        Object.entries(originalCategories).forEach(([name, amount]) => {
          updateCategory(name, amount, originalTotal);
        });

        if (revisedBudgetElement) {
          revisedBudgetElement.textContent = `₹${Math.round(originalTotal).toLocaleString("en-IN")}`;
        }

        if (potentialSavings) {
          potentialSavings.textContent = "₹0";
        }

        await updateStayRecommendations(tripData.dataset.accommodation);

        changesApplied = false;
      });
    }

    updateSavings();
  }

  // =========================================
  // 4. INTERACTIVE TRAVEL NOTEBOOK
  // =========================================

  const itineraryElement = document.getElementById("itinerary-data");
  const notebook = document.querySelector(".notebook");

  if (itineraryElement && notebook && tripData) {
    let itinerary = JSON.parse(itineraryElement.textContent);

    const leftPage = document.getElementById("left-page");
    const rightPage = document.getElementById("right-page");

    const previousButton = document.querySelector(".left-arrow");
    const nextButton = document.querySelector(".right-arrow");

    const indicator = document.getElementById("spread-indicator");
    const resetButton = document.getElementById("reset-itinerary");

    const destination = tripData.dataset.destination;
    const days = tripData.dataset.days;

    const storageKey = `waywise-edits-${destination}-${days}`;

    let currentSpread = 0;

    function escapeHTML(value) {
      return String(value ?? "").replace(
        /[&<>"']/g,
        (char) =>
          ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;",
          })[char],
      );
    }

    function loadEdits() {
      try {
        const saved = JSON.parse(localStorage.getItem(storageKey) || "{}");

        itinerary.forEach((day, dayIndex) => {
          day.activities.forEach((activity, activityIndex) => {
            const key = `${dayIndex}-${activityIndex}`;

            if (saved[key] !== undefined) {
              activity.activity = saved[key];
            }
          });
        });
      } catch (error) {
        console.error("Could not load itinerary edits:", error);
      }
    }

    function saveEdits() {
      const saved = {};

      itinerary.forEach((day, dayIndex) => {
        day.activities.forEach((activity, activityIndex) => {
          saved[`${dayIndex}-${activityIndex}`] = activity.activity;
        });
      });

      try {
        localStorage.setItem(storageKey, JSON.stringify(saved));
      } catch (error) {
        console.error("Could not save itinerary edits:", error);
      }
    }

    function createDayHTML(day, dayIndex) {
      let html = `
                <div class="notebook-day">
                    <span class="notebook-day-label">DAY ${escapeHTML(day.day)}</span>
                    <h2>${escapeHTML(day.title)}</h2>
                    <div class="notebook-activities">
            `;

      day.activities.forEach((activity, activityIndex) => {
        html += `
                    <div class="notebook-activity">
                        <span class="activity-time">
                            ${escapeHTML(activity.time)}
                        </span>
                        <p
                            class="editable-activity"
                            contenteditable="true"
                            data-day="${dayIndex}"
                            data-activity="${activityIndex}"
                            spellcheck="true"
                        >${escapeHTML(activity.activity)}</p>
                    </div>
                `;
      });

      html += `</div>`;

      if (day.tip) {
        html += `
                    <div class="notebook-note">
                        <strong>WayWise tip</strong>
                        <p>${escapeHTML(day.tip)}</p>
                    </div>
                `;
      }

      html += `</div>`;

      return html;
    }

    function createOverviewHTML() {
      return `
                <div class="notebook-cover">
                    <span class="section-kicker">WAYWISE TRAVEL JOURNAL</span>
                    <h2>Your Journey Begins</h2>
                    <p>Your personalised travel plan for ${escapeHTML(destination)}.</p>

                    <div class="notebook-note">
                        <p><strong>Destination:</strong> ${escapeHTML(destination)}</p>
                        <p><strong>Duration:</strong> ${escapeHTML(days)} days</p>
                        <p><strong>Travellers:</strong> ${escapeHTML(tripData.dataset.travellers)}</p>
                        <p><strong>Budget:</strong> ₹${Number(tripData.dataset.budget).toLocaleString("en-IN")}</p>
                    </div>
                </div>
            `;
    }

    const spreads = [];

    spreads.push({
      left: createOverviewHTML(),
      right: itinerary.length
        ? createDayHTML(itinerary[0], 0)
        : `
                <h2>Your journey awaits</h2>
            `,
      label: "Your trip overview",
    });

    for (let i = 1; i < itinerary.length; i += 2) {
      spreads.push({
        left: createDayHTML(itinerary[i], i),
        right: itinerary[i + 1]
          ? createDayHTML(itinerary[i + 1], i + 1)
          : `
                        <div class="notebook-cover">
                            <h2>Journey Complete</h2>
                            <p>May your next discovery be just around the corner.</p>
                        </div>
                    `,
        label: `Days ${i + 1}–${Math.min(i + 2, itinerary.length)}`,
      });
    }

    function showSpread() {
      const spread = spreads[currentSpread];

      leftPage.innerHTML = spread.left;
      rightPage.innerHTML = spread.right;

      if (indicator) {
        indicator.textContent = spread.label;
      }

      if (previousButton) {
        previousButton.disabled = currentSpread === 0;
      }

      if (nextButton) {
        nextButton.disabled = currentSpread === spreads.length - 1;
      }
    }

    loadEdits();

    // Rebuild spreads after loading saved edits
    spreads.length = 0;

    spreads.push({
      left: createOverviewHTML(),
      right: itinerary.length ? createDayHTML(itinerary[0], 0) : "",
      label: "Your trip overview",
    });

    for (let i = 1; i < itinerary.length; i += 2) {
      spreads.push({
        left: createDayHTML(itinerary[i], i),
        right: itinerary[i + 1]
          ? createDayHTML(itinerary[i + 1], i + 1)
          : `
                        <div class="notebook-cover">
                            <h2>Journey Complete</h2>
                            <p>May your next discovery be just around the corner.</p>
                        </div>
                    `,
        label: `Days ${i + 1}–${Math.min(i + 2, itinerary.length)}`,
      });
    }

    if (previousButton) {
      previousButton.addEventListener("click", function () {
        if (currentSpread > 0) {
          currentSpread--;
          showSpread();
        }
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", function () {
        if (currentSpread < spreads.length - 1) {
          currentSpread++;
          showSpread();
        }
      });
    }

    notebook.addEventListener("input", function (event) {
      const target = event.target;

      if (!target.classList.contains("editable-activity")) return;

      const dayIndex = Number(target.dataset.day);
      const activityIndex = Number(target.dataset.activity);

      const editedText = target.textContent.trim();

      if (
        itinerary[dayIndex] &&
        itinerary[dayIndex].activities[activityIndex]
      ) {
        itinerary[dayIndex].activities[activityIndex].activity = editedText;

        saveEdits();
      }
    });

    if (resetButton) {
      resetButton.addEventListener("click", function () {
        try {
          localStorage.removeItem(storageKey);
        } catch (error) {}

        window.location.reload();
      });
    }

    showSpread();
  }

  // =========================================
  // 5. DOWNLOAD ITINERARY AS PDF
  // =========================================

  const downloadButton = document.getElementById("download-pdf");

  if (downloadButton && tripData && itineraryElement) {
    downloadButton.addEventListener("click", async function () {
      const originalText = downloadButton.textContent;

      try {
        downloadButton.disabled = true;
        downloadButton.textContent = "Preparing PDF...";

        const destination = tripData.dataset.destination;
        const days = tripData.dataset.days;

        // Read itinerary, including saved edits
        const itinerary = JSON.parse(itineraryElement.textContent);

        const storageKey = `waywise-edits-${destination}-${days}`;

        const savedEdits = JSON.parse(localStorage.getItem(storageKey) || "{}");

        itinerary.forEach((day, dayIndex) => {
          day.activities.forEach((activity, activityIndex) => {
            const key = `${dayIndex}-${activityIndex}`;

            if (savedEdits[key] !== undefined) {
              activity.activity = savedEdits[key];
            }
          });
        });

        // Read current budget
        const originalBudget = Number(tripData.dataset.budget) || 0;

        const revisedBudgetText =
          document.getElementById("revised-budget")?.textContent || "0";

        const revisedBudget =
          Number(revisedBudgetText.replace(/[^\d.]/g, "")) || originalBudget;

        const savings = Math.max(0, originalBudget - revisedBudget);

        // Read budget categories
        const budgetCategories = [];

        document.querySelectorAll(".budget-category").forEach((category) => {
          const name = category
            .querySelector(".budget-category-heading span")
            ?.textContent.trim();

          const amountText =
            category.querySelector(".budget-category-heading strong")
              ?.textContent || "0";

          const amount = Number(amountText.replace(/[^\d.]/g, "")) || 0;

          if (name) {
            budgetCategories.push({
              name: name,
              amount: amount,
            });
          }
        });

        // Read destination recommendations only
        const places = [];

        document
          .querySelectorAll(
            ".recommendation-grid:not(.stay-grid) .recommendation-card",
          )
          .forEach((card) => {
            places.push({
              name:
                card.querySelector("h3, h4, strong")?.textContent.trim() || "",
              description: card.querySelector("p")?.textContent.trim() || "",
              type: "Destination discovery",
              area: "",
            });
          });

        // Read current accommodation recommendations
        const stays = [];

        document
          .querySelectorAll("#stay-grid .recommendation-card")
          .forEach((card) => {
            stays.push({
              name:
                card.querySelector("h3, h4, strong")?.textContent.trim() || "",
              best_for: card.querySelector("p")?.textContent.trim() || "",
              type:
                card.querySelector(".recommendation-tag")?.textContent.trim() ||
                "",
              area:
                card
                  .querySelector(".recommendation-meta span")
                  ?.textContent.trim() || "",
              url: card.querySelector("a")?.href || "",
            });
          });

        // Prepare data for Flask
        const payload = {
          destination: destination,
          days: days,
          travellers: tripData.dataset.travellers,
          budget: originalBudget,
          savings: savings,
          accommodation: tripData.dataset.accommodation,
          pace: tripData.dataset.pace || "Not specified",
          itinerary: itinerary,
          budget_categories: budgetCategories,
          places: places,
          stays: stays,
        };

        // Generate PDF
        const response = await fetch("/download-itinerary", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error("Could not generate the PDF.");
        }

        const pdfBlob = await response.blob();
        const pdfUrl = URL.createObjectURL(pdfBlob);

        const link = document.createElement("a");
        link.href = pdfUrl;
        link.download = `WayWise-${destination.replace(/\s+/g, "-")}-Itinerary.pdf`;

        document.body.appendChild(link);
        link.click();
        link.remove();

        URL.revokeObjectURL(pdfUrl);
      } catch (error) {
        console.error("PDF download error:", error);

        alert(
          "Sorry! We couldn't generate your itinerary PDF. Please try again.",
        );
      } finally {
        downloadButton.disabled = false;
        downloadButton.textContent = originalText;
      }
    });
  }
});
