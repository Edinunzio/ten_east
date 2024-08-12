"use strict";
class CardNavigator {
    constructor(totalCards = 3) {
        this.currentCard = 1;
        this.totalCards = totalCards;
    }
    init() {
        this.preventFormSubmissionOnEnter();
        this.showCard(this.currentCard);
        this.setupEventListeners();
    }
    preventFormSubmissionOnEnter() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                }
            });
        });
    }
    setupEventListeners() {
        document.querySelectorAll('.next-button').forEach(button => {
            button.addEventListener('click', () => this.nextCard());
        });
        document.querySelectorAll('.previous-button').forEach(button => {
            button.addEventListener('click', () => this.previousCard());
        });
    }
    allCheckboxesChecked(cardNumber) {
        const checkboxes = document.querySelectorAll(`#card-${cardNumber} input[type="checkbox"]`);
        return [...checkboxes].every(checkbox => checkbox.checked);
    }
    updateNextButtonState(cardNumber) {
        const nextButton = document.querySelector(`#card-${cardNumber} .next-button`);
        if (nextButton) {
            nextButton.disabled = !this.allCheckboxesChecked(cardNumber);
        }
    }
    showCard(cardNumber) {
        document.querySelectorAll('.card').forEach(card => card.style.display = 'none');
        const currentCardElement = document.getElementById(`card-${cardNumber}`);
        if (currentCardElement) {
            currentCardElement.style.display = 'block';
            this.updateNextButtonState(cardNumber);
            currentCardElement.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.addEventListener('change', () => this.updateNextButtonState(cardNumber));
            });
        }
    }
    nextCard() {
        if (this.currentCard === 1) {
            const amountInput = document.querySelector('#card-1 input[name="amount"]');
            const displayAmount = document.getElementById('display-amount');
            if (amountInput && displayAmount) {
                const amountValue = parseFloat(amountInput.value);
                if (isNaN(amountValue) || amountValue < 100000) {
                    alert("The minimum is 100,000.");
                    return;
                }
                displayAmount.textContent = amountInput.value;
            }
        }
        if (this.currentCard < this.totalCards) {
            this.currentCard++;
            this.showCard(this.currentCard);
        }
    }
    previousCard() {
        if (this.currentCard > 1) {
            this.currentCard--;
            this.showCard(this.currentCard);
        }
    }
}
class FormHandler {
    constructor() {
        this.setupEventListeners();
    }
    setupEventListeners() {
        const allocationForm = document.getElementById('form-allocations');
        const referralForm = document.getElementById('form-referral');
        if (allocationForm) {
            allocationForm.addEventListener('submit', (event) => {
                event.preventDefault();
            });
        }
        if (referralForm) {
            referralForm.addEventListener('submit', (event) => {
                event.preventDefault();
                this.submitReferralForm();
            });
        }
        const submitButton = document.querySelector('.submit-allocations');
        if (submitButton) {
            submitButton.addEventListener('click', () => this.submitAllocationForm());
        }
    }
    collectFormData(formId) {
        const inputs = document.querySelectorAll(`#${formId} input:not([type="checkbox"])`);
        return [...inputs].reduce((formData, input) => {
            const inputElement = input;
            formData[inputElement.name] = inputElement.value;
            return formData;
        }, {});
    }
    submitAllocationForm() {
        const data = this.collectFormData('form-allocations');
        console.log(data);
        fetch('/create-request-allocation/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
            if (data.status === 'success') {
                console.log('Request Allocation created successfully:', data);
                const formElement = document.getElementById('form-allocations');
                if (formElement) {
                    formElement.style.display = 'none';
                }
                const successMessage = document.getElementById('success-message');
                if (successMessage) {
                    successMessage.style.display = 'block';
                }
            }
            else {
                console.error('Error:', data.message);
            }
        })
            .catch((error) => {
            console.error('Error:', error);
        });
    }
    submitReferralForm() {
        const referralForm = document.getElementById('form-referral');
        const formData = new FormData(referralForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        console.log(data);
        fetch('/create-referral/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            },
            body: JSON.stringify(data),
        })
            .then(response => {
            if (response.ok) {
                alert('Your referral has been submitted');
                this.resetForm(referralForm);
            }
            else {
                console.error('Failed to submit referral form:', response.statusText);
                alert('This referral has already been made.');
                this.resetForm(referralForm);
            }
        })
            .catch(error => {
            console.error('Error submitting referral form:', error);
        });
    }
    resetForm(form) {
        form.reset();
    }
    getCsrfToken() {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return csrfToken ? csrfToken.value : '';
    }
}
document.addEventListener('DOMContentLoaded', () => {
    const cardNavigator = new CardNavigator(3);
    cardNavigator.init();
    const formHandler = new FormHandler();
});
//# sourceMappingURL=app.js.map