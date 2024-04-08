var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-span',
    data() {
        return {
            root: root,
            currentQuestion: {},
            userId: document.body.getAttribute('data-user-id') || null,
            problem: {
                milestones: [] // Initialize milestones as an empty array
            },
            question: {},
            resource: {},
            activeTab: 'understand',
            buttonDisabled: false,
        }
    },
    computed: {
        minutes() {
            if (!this.currentQuestion.timer) return '00';
            return Math.floor(this.currentQuestion.timer / 60).toString().padStart(2, '0');
        },
        seconds() {
            if (!this.currentQuestion.timer) return '00';
            return (this.currentQuestion.timer % 60).toString().padStart(2, '0');
        }
    },
    mounted: async function () {
        await this.fetchProblem();
        this.setActiveTab(this.activeTab);
        this.startTimerForCurrentQuestion();
    },
    watch: {
      question: function (newQuestion, oldQuestion) {
        this.$nextTick(() => {
            this.initializeSwiper();
        });
      },
    },
    methods: {
        renderMarkdown(markdownText) {
            return marked.parse(markdownText);
        },
        setActiveTab(tabName) {
        this.activeTab = tabName;
        // Check if the selected tab has questions
        if (this.problem && this.problem.questions && this.problem.questions[tabName]) {
            // Cleanup before changing the question
            if (this.currentQuestion.timerInterval) {
                clearInterval(this.currentQuestion.timerInterval);
            }

            this.question = this.problem.questions[tabName];
            this.currentQuestion = this.question[0] || {};

            // Setup after changing the question
            if (this.currentQuestion.timerRunning) {
                this.startTimerForCurrentQuestion();
            }
        } else {
            this.question = [];
            this.currentQuestion = {};
        }
        this.$nextTick(() => {
            this.initializeSwiper();
        });
    },
        initializeSwiper() {
    if (this.swiperInstance && typeof this.swiperInstance.destroy === 'function') {
        this.swiperInstance.destroy(true, true); // Pass true to both parameters for a complete cleanup
    }
    this.$nextTick(() => {
        if (this.question && this.question.length > 0) {
            this.swiperInstance = new Swiper('.swiper-container', {
                slidesPerView: 1,
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                on: {
                    slideChange: () => {
                        if (this.currentQuestion.timerInterval) {
                            clearInterval(this.currentQuestion.timerInterval);
                        }
                        this.currentQuestion = this.question[this.swiperInstance.activeIndex];
                        if (this.currentQuestion.timerRunning) {
                            this.startTimerForCurrentQuestion();
                        }
                    }
                }
            });
        }
    });
},
        fetchProblem() {
            return axios.get(this.root + '/api/problem/?name=' + problem_name)
                .then(response => {
                    if (response.data && response.data.length > 0) {
                        const problemData = response.data[0];
                        Object.keys(problemData.questions).forEach(category => {
                            problemData.questions[category].forEach(question => {
                                if(question.q_type === 2) {
                                    question.selectedChoices = "";
                                    question.timer = 120;
                                } else {
                                    question.selectedChoices = new Array(question.desc.choice.length).fill(false);
                                    question.timer = 60;
                                }
                                question.showExplanation = false;
                                question.isCorrect = false;
                                question.isSubmitted = false;
                                question.timerRunning = true;
                            });
                        });
                        this.problem = problemData;
                    } else {
                        this.message = 'An error occurred while fetching the problem.';
                    }
                })
                .catch(error => {
                    this.message = 'An error occurred while fetching the problem.';
                });
        },
        submitQuestion() {
            let timeSpent = Math.max(0, 60 - this.currentQuestion.timer);
            if(question.q_type === 0) {
                let selectedChoices = this.getSelectedChoices();
                let isCorrect = this.checkAnswer(selectedChoices);
                let submissionData = {
                    user: this.userId,
                    problem_id: this.problem.id,
                    question_id: this.currentQuestion.id,
                    is_correct: isCorrect,
                    time_spent: timeSpent,
                    content: {
                        selectedChoices: selectedChoices,
                    }
                };
            }
            const config = {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            };
            axios.post('/api/submission/', submissionData, config)
                .then(response => {
                    this.currentQuestion.showExplanation = true;
                    this.currentQuestion.isCorrect = isCorrect ? "Correct" : "Incorrect";
                    this.currentQuestion.isSubmitted = true;
                    if (this.currentQuestion.timerInterval) {
                        clearInterval(this.currentQuestion.timerInterval);
                    }
                    this.fetchAndUpdateMilestones();
                })
                .catch(error => {
                    console.error("Submission failed", error);
                    // Handle error
                });
        },
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
        fetchAndUpdateMilestones() {
            return axios.get(this.root + '/api/problem/?name=' + problem_name)
                .then(response => {
                    if (response.data && response.data.length > 0) {
                        const problemData = response.data[0];
                        Object.keys(problemData.questions).forEach(category => {
                            problemData.questions[category].forEach(question => {
                            });
                        });
                        this.problem.milestones = problemData.milestones;
                    } else {
                        this.message = 'An error occurred while fetching the problem.';
                    }
                })
                .catch(error => {
                    this.message = 'An error occurred while fetching the problem.';
                });
        },
        startTimerForCurrentQuestion() {
    if (this.currentQuestion.timerInterval) {
        clearInterval(this.currentQuestion.timerInterval);
    }
    this.currentQuestion.timerInterval = setInterval(() => {
        if (this.currentQuestion.timer > 0) {
            this.currentQuestion.timer--;
        } else {
            clearInterval(this.currentQuestion.timerInterval);
            // Optionally, handle what happens when the timer reaches 0
        }
    }, 1000);
},
        toggleTimer() {
    this.currentQuestion.timerRunning = !this.currentQuestion.timerRunning;
    if (this.currentQuestion.timerRunning) {
        this.startTimerForCurrentQuestion();
    } else {
        clearInterval(this.currentQuestion.timerInterval);
    }
},
    },
    beforeDestroy() {
    this.problem.questions.forEach(category => {
        category.forEach(question => {
            if (question.timerInterval) {
                clearInterval(question.timerInterval);
            }
        });
    });
},
});
