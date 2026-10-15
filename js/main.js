const INQUIRE_EMAIL = "inquiries@villagiaggioli.com";

const header = document.querySelector("[data-header]");
const nav = document.querySelector("[data-nav]");
const toggle = document.querySelector("[data-nav-toggle]");
const form = document.querySelector("[data-inquire-form]");
const status = document.querySelector("[data-form-status]");
const year = document.querySelector("[data-year]");

if (year) {
  year.textContent = String(new Date().getFullYear());
}

const setNav = (open) => {
  document.body.classList.toggle("nav-open", open);
  toggle?.setAttribute("aria-expanded", String(open));
};

toggle?.addEventListener("click", () => {
  setNav(!document.body.classList.contains("nav-open"));
});

nav?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => setNav(false));
});

window.addEventListener("scroll", () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 8);
}, { passive: true });

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setNav(false);
});

const formatDate = (value) => {
  if (!value) return "Not specified";
  const date = new Date(`${value}T00:00:00`);
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(date);
};

form?.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const name = String(data.get("name") || "").trim();
  const email = String(data.get("email") || "").trim();
  const message = String(data.get("message") || "").trim();
  const guests = String(data.get("guests") || "").trim();

  if (!name || !email || !message) {
    if (status) {
      status.hidden = false;
      status.classList.add("is-error");
      status.textContent = "Please add your name, email, and a short message.";
    }
    return;
  }

  const body = [
    `Name: ${name}`,
    `Email: ${email}`,
    `Arrival: ${formatDate(String(data.get("arrive") || ""))}`,
    `Departure: ${formatDate(String(data.get("depart") || ""))}`,
    `Guests: ${guests || "Not specified"}`,
    "",
    message,
  ].join("\n");

  const href = `mailto:${INQUIRE_EMAIL}?subject=${encodeURIComponent(`Villa Giaggioli inquiry from ${name}`)}&body=${encodeURIComponent(body)}`;

  if (status) {
    status.hidden = false;
    status.classList.remove("is-error");
    status.textContent = "Opening your email application…";
  }

  window.location.href = href;
});
