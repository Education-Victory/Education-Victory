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
      isSubmitting: false,
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
    fetchProblem() {
      return axios.get(this.root + '/api/problem/?name=' + problem_name)
        .then(response => {
          if (response.data && response.data.length > 0) {
            const problemData = response.data[0];
            Object.keys(problemData.questions).forEach(category => {
              problemData.questions[category].forEach(question => {
                if (question.q_type === 2) {
                  question.textareaContent = "";
                  question.defaultTimer = 120;
                  question.timer = 120;
                } else {
                  question.selectedChoices = new Array(question.desc.choice.length).fill(false);
                  question.defaultTimer = 60;
                  question.timer = 60;
                }
                question.showExplanation = false;
                question.grade = 0;
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
    submitQuestion: async function() {
      this.isSubmitting = true; // Start loading state
      this.cleanupTimer(); // Stop the timer as soon as the submission starts

      let timeSpent = Math.max(0, this.currentQuestion.defaultTimer - this.currentQuestion.timer);
      this.currentQuestion.submitContent = this.getContent();
      
      try {
        // Await the resolution of the Promise returned by checkAndReview
        const [grade, tip] = await this.checkAndReview(this.currentQuestion.submitContent);
        this.currentQuestion.grade = grade;
        this.currentQuestion.tip = tip;
        
        let submissionData = {
          user: this.userId,
          problem_id: this.problem.id,
          question_id: this.currentQuestion.id,
          q_type: this.currentQuestion.q_type,
          g_type: this.currentQuestion.grade,
          time_spent: timeSpent,
          content: {
            submit_content: this.currentQuestion.submitContent,
            tip: this.currentQuestion.tip,
          },
        };
        const config = {
          headers: {
            'X-CSRFToken': csrfToken
          }
        };
        await axios.post('/api/submission/', submissionData, config);
        
        this.currentQuestion.showExplanation = true;
        this.currentQuestion.isSubmitted = true;
        this.fetchAndUpdateMilestones();
      } catch (error) {
        console.error("Submission failed", error);
      } finally {
        this.isSubmitting = false;
        this.currentQuestion.isSubmitted = true;
      }
    },
    async checkAndReview(submitContent) {
      let grade;
      let tip;
      
      if (this.currentQuestion.q_type === 0) {
        const selectedChoices = this.getSelectedChoices();
        const correctAnswer = this.currentQuestion.desc.answer;
        grade = selectedChoices === correctAnswer ? 'Excellent' : 'Weak';
      }

      try {
        // Await the response from apiReview
        const response = await this.apiReview(submitContent);
        if (this.currentQuestion.q_type !== 0) {
          grade = response.data.grade !== undefined ? response.data.grade : 'Good';
        }
        tip = response.data.tip;
        
      } catch (error) {
        console.error("Review failed", error);
        // Handle error, for example, by setting default values or showing an error message
      }

      return [grade, tip];
    },
    apiReview(submitContent) {
      let reviewData = {
        user: this.userId,
        problem_id: this.problem.id,
        question_id: this.currentQuestion.id,
        q_type: this.currentQuestion.q_type,
        content: submitContent,
      };
      const config = {
        headers: {
          'X-CSRFToken': csrfToken
        }
      };
      return axios.post('/api/review/', reviewData, config);
    },
    fetchAndUpdateMilestones() {
      return axios.get(this.root + '/api/problem/?name=' + problem_name)
        .then(response => {
          if (response.data && response.data.length > 0) {
            const problemData = response.data[0];
            Object.keys(problemData.questions).forEach(category => {
              problemData.questions[category].forEach(question => {});
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
    getContent() {
      let content;
      if (this.currentQuestion.q_type === 0) {
          content = this.getSelectedChoices();
      } else {
          content = this.currentQuestion.textareaContent;
      }
      return content;
    },
    isGradeSuccess(grade) {
      return grade === 'Excellent' || grade === 'Good'; // Returns true for 'Excellent' and 'Good'
    },
    renderMarkdown(markdownText) {
      return marked.parse(markdownText);
    },
    setActiveTab(tabName) {
      this.activeTab = tabName;
      this.updateQuestionBasedOnTab();
    },
    updateQuestionBasedOnTab() {
      const tabQuestions = this.problem.questions ? this.problem.questions[this.activeTab] : null;
      this.question = tabQuestions || [];
      this.currentQuestion = this.question.length ? this.question[0] : {};
      this.cleanupTimer();
      if (this.currentQuestion.timerRunning) {
        this.startTimerForCurrentQuestion();
      }
      this.$nextTick(() => {
        this.initializeSwiper();
      });
    },
    cleanupTimer() {
      if (this.currentQuestion.timerInterval) {
        clearInterval(this.currentQuestion.timerInterval);
      }
    },
        startTimerForCurrentQuestion() {
      this.cleanupTimer();
      this.currentQuestion.timerInterval = setInterval(() => {
        if (this.currentQuestion.timer > 0) {
          this.currentQuestion.timer--;
        } else {
          clearInterval(this.currentQuestion.timerInterval);
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
