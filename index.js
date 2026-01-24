const contactForm = document.getElementById('contact-form');
const contactList = document.getElementById('contact-list');
const searchForm = document.getElementById('search-form');
const contactIdInput = document.getElementById('contact-id');
const nomInput = document.getElementById('nom');
const prenomInput = document.getElementById('prenom');
const emailInput = document.getElementById('email');
const telInput = document.getElementById('tel');
const adresseInput = document.getElementById('adresse');
const adresseTravailInput = document.getElementById('adresse_travail');
const forgetChoiceButton = document.getElementById('forget-choice');

// Récupérer tous les contacts et les afficher
function loadContacts() {
  window.api.fetch('/api/contacts')
    .then(contacts => {
      contactList.innerHTML = '';
      contacts.forEach(contact => {
        const li = document.createElement('li');
        li.innerHTML = `
          ${contact.nom} ${contact.prenom} - ${contact.email}
          <button onclick="editContact(${contact.id})">Modifier</button>
          <button onclick="deleteContact(${contact.id})">Supprimer</button>
        `;
        contactList.appendChild(li);
      });
    });
}

// Gérer la soumission du formulaire de contact
contactForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const id = contactIdInput.value;
  const contactData = {
    nom: nomInput.value,
    prenom: prenomInput.value,
    email: emailInput.value,
    telephone: telInput.value,
    adresse: adresseInput.value,
    adresse_travail: adresseTravailInput.value,
  };

  if (id) {
    // Mettre à jour le contact existant
    window.api.fetch(`/api/contacts/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(contactData),
    }).then(() => {
      contactForm.reset();
      loadContacts();
    });
  } else {
    // Ajouter un nouveau contact
    window.api.fetch('/api/contacts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(contactData),
    }).then(() => {
      contactForm.reset();
      loadContacts();
    });
  }
});

// Gérer la soumission du formulaire de recherche
searchForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const searchTerm = document.getElementById('search-term').value;
  window.api.fetch(`/api/contacts/search?q=${searchTerm}`)
    .then(contacts => {
      contactList.innerHTML = '';
      contacts.forEach(contact => {
        const li = document.createElement('li');
        li.innerHTML = `
          ${contact.nom} ${contact.prenom} - ${contact.email}
          <button onclick="editContact(${contact.id})">Modifier</button>
          <button onclick="deleteContact(${contact.id})">Supprimer</button>
        `;
        contactList.appendChild(li);
      });
    });
});

// Supprimer un contact
function deleteContact(id) {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce contact ?')) {
    window.api.fetch(`/api/contacts/${id}`, { method: 'DELETE' })
      .then(() => loadContacts());
  }
}

// Remplir le formulaire pour la modification
function editContact(id) {
  window.api.fetch(`/api/contacts/${id}`)
    .then(contact => {
      contactIdInput.value = contact.id;
      nomInput.value = contact.nom;
      prenomInput.value = contact.prenom;
      emailInput.value = contact.email;
      telInput.value = contact.telephone;
      adresseInput.value = contact.adresse;
      adresseTravailInput.value = contact.adresse_travail;
    });
}

// Charger les contacts lorsque l'URL de la base de données est définie
window.api.on('db-url', () => {
    loadContacts();
});

// Écouteur d'événements pour le bouton "Oublier le choix de la base de données"
forgetChoiceButton.addEventListener('click', () => {
    if (confirm('Are you sure you want to forget your database choice and restart the application?')) {
        window.api.forgetDbChoice();
    }
});
