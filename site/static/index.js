let onlyWinners = false;

function generateProjectCardHtml(project) {
  return `
    <div>
      ${project.winner ? '<div class="winner-banner"><img src="/winner.png"/></div>' : ''}
    <div class="project">
      <div class="project-image"></div>
      <div class="project-caption">
        <div class="project-header">${ project.title }</div>
        <div class="project-tagline">${ project.tagline }</div>
      </div>
      <div class="project-footer">
        <div><span class="material-icons icon">favorite</span> ${ project.likes }</div>
        <div><span class="material-icons icon">chat</span> ${ project.comments }</div>
      </div>
    </div>
  </div>`
}

async function populateProjects() {
  const response = await fetch('/projects.json');
  const projects = (await response.json()).projects;
  let html = '';
  for (const project of projects.filter(it => !onlyWinners || it.winner == true)) {
    html += generateProjectCardHtml(project);
  }
  const projectContainer = document.getElementById("projects");
  projectContainer.innerHTML = html;
}

function onOnlyWinnersPressed() {
  onlyWinners = !onlyWinners;
  const button = document.getElementById('winners');
  button.className = onlyWinners ? 'checked' : ''
  populateProjects();
}