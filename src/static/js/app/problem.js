var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-span',
    data() {
        return {
            root: root,
            currentQuestion: {},
            problem: {
                milestones: [] // Initialize milestones as an empty array
            },
            question: {},
            resource: {},
            activeTab: 'understand',
        }
    },
    watch: {
        question: function (newQuestion, oldQuestion) {
            this.$nextTick(() => {
                this.initializeSwiper();
            });
        }
    },
    mounted: async function () {
        await this.fetchProblem();
        this.setActiveTab(this.activeTab);
    },
    methods: {
        renderMarkdown(markdownText) {
            return marked.parse(markdownText);
        },
        setActiveTab(tabName) {
            this.activeTab = tabName;
            // Ensure 'problem' and 'problem.questions' are defined before accessing
            if (this.problem && this.problem.questions && this.problem.questions[tabName]) {
                this.question = this.problem.questions[tabName];
                this.currentQuestion = this.question[0];
            } else {
                this.question = [];
            }
        },
        fetchProblem() {
            return axios.get(this.root + '/api/problem/?name=' + problem_name)
                .then(response => {
                    if (response.data && response.data.length > 0) {
                        const problemData = response.data[0];
                        Object.keys(problemData.questions).forEach(category => {
                            problemData.questions[category].forEach(question => {
                                question.selectedChoices = new Array(question.desc.choice.length).fill(false);
                                question.showExplanation = false;
                                question.isCorrect = false;
                            });
                        });
                        this.problem = problemData;
                    } else {
                        this.message = 'An error occurred while fetching the problem.';
                    }
                })
                .catch(error => {
                    console.error("There was an error fetching the problem:", error);
                    this.message = 'An error occurred while fetching the problem.';
                });
        },
        initializeSwiper() {
            if (this.swiperInstance) {
                this.swiperInstance.destroy();
            }
            this.$nextTick(() => {
                this.swiperInstance = new Swiper('.swiper-container', {
                    slidesPerView: 1,
                    pagination: {
                        el: '.swiper-pagination',
                        clickable: true,
                    },
                    on: {
                        slideChange: () => {
                            this.currentQuestion = this.question[this.swiperInstance.activeIndex];
                        }
                    }
                });
            });
        },
        submitQuestion() {
            let selectedChoices = this.getSelectedChoices();
            let isCorrect = this.checkAnswer(selectedChoices);
            this.currentQuestion.showExplanation = true;
            this.currentQuestion.isCorrect = isCorrect;
            let submissionData = {
                user: this.user.id,
                a_type: 0,
                content: {
                    problem: this.problem.id,
                    question: this.question.id,
                    selectedChoices: selectedChoices,
                    isCorrect: isCorrect
                }
            };
            axios.post('/api/useractivity/', submissionData)
                .then(response => {
                    // this.showExplanation = true;
                    // this.explanationText = this.currentQuestion.desc.explain;
                    console.log("Submission successful", response.data);
                    // Handle success (e.g., show a message to the user)
                })
                .catch(error => {
                    console.error("Submission failed", error);
                    // Handle error
                });
        },
        resetQuestion() {},
        getSelectedChoices() {
            let selectedLabels = '';
            this.currentQuestion.selectedChoices.forEach((isSelected, index) => {
                if (isSelected) {
                    const label = String.fromCharCode('A'.charCodeAt(0) + index);
                    selectedLabels += label;
                }
            });

            // Return the concatenated string of selected choice labels
            return selectedLabels;
        },
       checkAnswer(selectedChoices) {
            const correctAnswer = this.currentQuestion.desc.answer;
            return selectedChoices === correctAnswer;
        },
        resetQuestion() {
            // Reset all checkboxes for the current question to unchecked.
            const choices = this.currentQuestion.desc.choice;
            choices.forEach((_, index) => {
                const checkbox = document.querySelector(`input[name="question-${this.currentQuestion.id}-choice-${index}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                }
            });
        },
    }
});
