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
const clearSearchBtn = document.getElementById('clear-search-btn');

function loadContacts() {
  window.api.fetch('/api/contacts')
    .then(contacts => {
      contactList.innerHTML = '';
      contacts.forEach(contact => {
        const li = document.createElement('li');
        li.innerHTML = `
          <div class="contact-info">
              <strong>${contact.nom} ${contact.prenom}</strong><br>
              Email: ${contact.email}<br>
              Téléphone: ${contact.telephone}<br>
              Adresse: ${contact.adresse}<br>
              Adresse de travail: ${contact.adresse_travail}
          </div>
          <div class="actions">
              <button class="edit-btn" onclick="editContact(${contact.id})">Modifier</button>
              <button class="delete-btn" onclick="deleteContact(${contact.id})">Supprimer</button>
          </div>
        `;
        contactList.appendChild(li);
      });
    });
}

// Gérer la soumission du formulaire de contact
contactForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const id = contactIdInput.value;
  const submitButton = contactForm.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;
  
  // Ajouter l'animation de sauvegarde
  submitButton.classList.add('saving');
  submitButton.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg><span class="spinner"></span>';
  submitButton.disabled = true;
  
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
      const successMessage = document.createElement('div');
      successMessage.classList.add('success-message');
      successMessage.textContent = 'Contact mis à jour avec succès!';
      contactForm.prepend(successMessage);
      setTimeout(() => {
        successMessage.remove();
      }, 3000);

      submitButton.classList.remove('saving');
      submitButton.textContent = 'Enregistrer';
      submitButton.disabled = false;
      const cancelButton = contactForm.querySelector('.cancel-btn');
      if (cancelButton) {
        cancelButton.remove();
      }
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
      const successMessage = document.createElement('div');
      successMessage.classList.add('success-message');
      successMessage.textContent = 'Contact ajouté avec succès!';
      contactForm.prepend(successMessage);
      setTimeout(() => {
        successMessage.remove();
      }, 3000);
      
      submitButton.classList.remove('saving');
      submitButton.textContent = 'Enregistrer';
      submitButton.disabled = false;
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
          <div class="contact-info">
              <strong>${contact.nom} ${contact.prenom}</strong><br>
              Email: ${contact.email}<br>
              Téléphone: ${contact.telephone}<br>
              Adresse: ${contact.adresse}<br>
              Adresse de travail: ${contact.adresse_travail}
          </div>
          <div class="actions">
              <button class="edit-btn" onclick="editContact(${contact.id})">Modifier</button>
              <button class="delete-btn" onclick="deleteContact(${contact.id})">Supprimer</button>
          </div>
        `;
        contactList.appendChild(li);
      });
    });
});

// Supprimer un contact
async function deleteContact(id) {
  if (await window.ipc.showConfirmationDialog('Êtes-vous sûr de vouloir supprimer ce contact ?')) {
    window.api.fetch(`/api/contacts/${id}`, { method: 'DELETE' })
      .then(() => {
        loadContacts();
        const successMessage = document.createElement('div');
        successMessage.classList.add('success-message');
        successMessage.textContent = 'Contact supprimé avec succès!';
        const contactListContainer = document.querySelector('.contact-list-container');
        contactListContainer.prepend(successMessage);
        setTimeout(() => {
          successMessage.remove();
        }, 3000);
      });
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

      const submitButton = contactForm.querySelector('button[type="submit"]');
      submitButton.textContent = 'Mettre à jour';

      let cancelButton = contactForm.querySelector('.cancel-btn');
      if (!cancelButton) {
        cancelButton = document.createElement('button');
        cancelButton.type = 'button';
        cancelButton.textContent = 'Annuler';
        cancelButton.classList.add('cancel-btn');
        submitButton.after(cancelButton);

        cancelButton.addEventListener('click', () => {
          contactForm.reset();
          contactIdInput.value = '';
          submitButton.textContent = 'Enregistrer';
          cancelButton.remove();
        });
      }
      
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Charger les contacts lorsque l'URL de la base de données est définie
window.api.once('db-url', () => {
    console.log('db-url event received in renderer process. Calling loadContacts().');
    loadContacts();
});

// Écouteur d'événements pour le bouton "Oublier le choix de la base de données"
forgetChoiceButton.addEventListener('click', async () => {
    if (await window.ipc.showConfirmationDialog('Are you sure you want to forget your database choice and restart the application?')) {
        window.api.forgetDbChoice();
    }
});

// Écouteur d'événements pour le bouton "Annuler la recherche"
clearSearchBtn.addEventListener('click', () => {
    document.getElementById('search-term').value = '';
    loadContacts();
});
