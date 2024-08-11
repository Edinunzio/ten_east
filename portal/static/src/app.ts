class CardNavigator {
    private currentCard: number;
    private totalCards: number;

    constructor() {
        this.currentCard = 1;
        this.totalCards = 3;
        this.init();
    }

    private init(): void {
        this.showCard(this.currentCard);
        this.setupEventListeners();
    }

    private setupEventListeners(): void {
        const form = document.getElementById('form-container') as HTMLFormElement;

        if (form) {
            form.addEventListener('submit', (event) => {
                event.preventDefault();
            });
        }
        const nextButtons = document.querySelectorAll('.next-button');
        document.querySelectorAll('.next-button').forEach(button => {
            button.addEventListener('click', () => this.nextCard());
        });

        document.querySelectorAll('.previous-button').forEach(button => {
            button.addEventListener('click', () => this.previousCard());
        });

        const submitButton = document.querySelector('.submit-button');
        if (submitButton) {
            submitButton.addEventListener('click', () => this.submitForm());
        }
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
            if (displayAmount && amountInput) {
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

    private collectFormData(): { [key: string]: string } {
        const inputs = document.querySelectorAll('#form-container input:not([type="checkbox"])');
        return [...inputs].reduce((formData: { [key: string]: string }, input) => {
            const inputElement = input as HTMLInputElement;
            formData[inputElement.name] = inputElement.value;
            return formData;
        }, {});
    }

    private submitForm(): void {
        const data = this.collectFormData();
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
                alert('success!');
                
                // Hide the form after successful submission
                const formElement = document.getElementById('form-container');
                if (formElement) {
                    formElement.style.display = 'none';
                }
    
                // Optionally, show a success message
                const successMessage = document.getElementById('success-message');
                if (successMessage) {
                    successMessage.style.display = 'block';
                }
            } else {
                console.error('Error:', data.message);
                // Optionally, display an error message to the user
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            // Optionally, display a generic error message to the user
        });
    }
    

    private getCsrfToken(): string {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]') as HTMLInputElement;
        return csrfToken ? csrfToken.value : '';
    }
}

const cardNavigator = new CardNavigator();
