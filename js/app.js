const state = { step: 1, answers: {} };
const form = document.querySelector('#planner-form');
const questions = [...document.querySelectorAll('.question')];
const progressLabel = document.querySelector('#progress-label');
const progressBar = document.querySelector('#progress-bar');
const prevButton = document.querySelector('#prev-button');
const nextButton = document.querySelector('#next-button');
const submitButton = document.querySelector('#submit-button');
const formError = document.querySelector('#form-error');
const resultSection = document.querySelector('#result-section');
const loadingState = document.querySelector('#loading-state');
const resultCard = document.querySelector('#result-card');
const apiError = document.querySelector('#api-error');

function updateStep() {
  questions.forEach((question) => question.classList.toggle('active', Number(question.dataset.step) === state.step));
  progressLabel.textContent = `0${state.step} / 04`;
  progressBar.style.width = `${state.step * 25}%`;
  prevButton.disabled = state.step === 1;
  nextButton.classList.toggle('hidden', state.step === 4);
  submitButton.classList.toggle('hidden', state.step !== 4);
  formError.textContent = '';
}

function requiredField() { return ['isOffWork', 'mood', 'fatigue', 'availableTime'][state.step - 1]; }

document.querySelectorAll('.choice').forEach((button) => {
  button.addEventListener('click', () => {
    const { field, value } = button.dataset;
    state.answers[field] = value;
    document.querySelectorAll(`.choice[data-field="${field}"]`).forEach((choice) => choice.classList.toggle('selected', choice === button));
    formError.textContent = '';
  });
});

nextButton.addEventListener('click', () => {
  if (!state.answers[requiredField()]) { formError.textContent = '가장 가까운 답을 하나 골라주세요.'; return; }
  state.step += 1; updateStep();
});
prevButton.addEventListener('click', () => { if (state.step > 1) { state.step -= 1; updateStep(); } });

function showResult(data) {
  document.querySelector('#result-title').textContent = data.title;
  document.querySelector('#result-summary').textContent = data.summary;
  document.querySelector('#result-tip-text').textContent = data.tip;
  document.querySelector('#closing-message').textContent = `“${data.closing_message}”`;
  const list = document.querySelector('#result-steps'); list.innerHTML = '';
  data.steps.forEach((step, index) => {
    const item = document.createElement('li');
    item.innerHTML = `<span>0${index + 1} · ${step.minutes}분</span><div><strong>${step.action}</strong><p>${step.description}</p></div>`;
    list.append(item);
  });
  loadingState.hidden = true; apiError.hidden = true; resultCard.hidden = false;
}

async function requestPlan() {
  resultSection.hidden = false; loadingState.hidden = false; resultCard.hidden = true; apiError.hidden = true;
  resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const payload = { ...state.answers, isOffWork: state.answers.isOffWork === 'true' };
    const response = await fetch('/api/recovery-plan', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload), signal: controller.signal });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.code || 'unknown'); 
    }
    showResult(await response.json());
  } catch (error) {
    loadingState.hidden = true; apiError.hidden = false;
    document.querySelector('#api-error p').textContent =
    `잠시 후 다시 시도해 주세요. (오류 코드: ${error.message})`;
  } finally { clearTimeout(timeout); }
}

form.addEventListener('submit', (event) => { event.preventDefault(); if (!state.answers[requiredField()]) { formError.textContent = '가장 가까운 답을 하나 골라주세요.'; return; } requestPlan(); });
document.querySelector('#retry-button').addEventListener('click', requestPlan);
document.querySelector('#restart-button').addEventListener('click', () => { state.step = 1; state.answers = {}; document.querySelectorAll('.choice').forEach((choice) => choice.classList.remove('selected')); resultSection.hidden = true; updateStep(); document.querySelector('#planner').scrollIntoView({ behavior: 'smooth' }); });
document.querySelector('.menu-toggle').addEventListener('click', (event) => { const nav = document.querySelector('.main-nav'); const open = nav.classList.toggle('open'); event.currentTarget.setAttribute('aria-expanded', String(open)); });
document.querySelectorAll('.main-nav a').forEach((link) => link.addEventListener('click', () => document.querySelector('.main-nav').classList.remove('open')));
updateStep();
