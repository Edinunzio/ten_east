class CardNavigator {
    private currentCard: number;
    private totalCards: number;

    constructor(totalCards: number = 3) {
        this.currentCard = 1;
        this.totalCards = totalCards;
    }

    public init(): void {
        this.preventFormSubmissionOnEnter();
        this.showCard(this.currentCard);
        this.setupEventListeners();
    }

    private preventFormSubmissionOnEnter(): void {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                }
            });
        });
    }

    private setupEventListeners(): void {
        document.querySelectorAll('.next-button').forEach(button => {
            button.addEventListener('click', () => this.nextCard());
        });

        document.querySelectorAll('.previous-button').forEach(button => {
            button.addEventListener('click', () => this.previousCard());
        });
    }

    private showCard(cardNumber: number): void {
        document.querySelectorAll('.card').forEach(card => (card as HTMLElement).style.display = 'none');
        const currentCardElement = document.getElementById(`card-${cardNumber}`);
        if (currentCardElement) {
            (currentCardElement as HTMLElement).style.display = 'block';

            this.updateNextButtonState(cardNumber);

            currentCardElement.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.addEventListener('change', () => this.updateNextButtonState(cardNumber));
            });
        }
    }

    private allCheckboxesChecked(cardNumber: number): boolean {
        const checkboxes = document.querySelectorAll(`#card-${cardNumber} input[type="checkbox"]`);
        return [...checkboxes].every(checkbox => (checkbox as HTMLInputElement).checked);
    }

    private updateNextButtonState(cardNumber: number): void {
        const nextButton = document.querySelector(`#card-${cardNumber} .next-button`) as HTMLButtonElement;
        if (nextButton) {
            nextButton.disabled = !this.allCheckboxesChecked(cardNumber);
        }
    }

    private nextCard(): void {
        if (this.currentCard === 1) {
            const amountInput = document.querySelector('#card-1 input[name="amount"]') as HTMLInputElement;
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

    private previousCard(): void {
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

    private setupEventListeners(): void {
        const allocationForm = document.getElementById('form-allocations') as HTMLFormElement;
        const referralForm = document.getElementById('form-referral') as HTMLFormElement;

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

    private collectFormData(formId: string): { [key: string]: string } {
        const inputs = document.querySelectorAll(`#${formId} input:not([type="checkbox"])`);
        return [...inputs].reduce((formData: { [key: string]: string }, input) => {
            const inputElement = input as HTMLInputElement;
            formData[inputElement.name] = inputElement.value;
            return formData;
        }, {});
    }

    private submitAllocationForm(): void {
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
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    private submitReferralForm(): void {
        const referralForm = document.getElementById('form-referral') as HTMLFormElement;
        const formData = new FormData(referralForm);

        const data: { [key: string]: any } = {};
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
            } else {
                console.error('Failed to submit referral form:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error submitting referral form:', error);
        });
    }

    private resetForm(form: HTMLFormElement): void {
        form.reset();
    }

    private getCsrfToken(): string {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]') as HTMLInputElement;
        return csrfToken ? csrfToken.value : '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const cardNavigator = new CardNavigator(3);
    cardNavigator.init();

    const formHandler = new FormHandler();
});
