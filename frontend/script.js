document.getElementById('submitBtn').addEventListener('click', async () => {
    const ticketText = document.getElementById('ticketInput').value.trim();
    if (!ticketText) return;

    const btn = document.getElementById('submitBtn');
    const pipeline = document.getElementById('pipeline');
    const steps = document.querySelectorAll('.step');
    
    // Reset UI
    btn.classList.add('loading');
    pipeline.style.display = 'flex';
    steps.forEach(step => step.classList.remove('visible'));
    
    try {
        const response = await fetch('/api/process_ticket', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ticket_text: ticketText })
        });

        if (!response.ok) throw new Error('API Error');
        const data = await response.json();

        // Reveal steps sequentially with a slight delay for visual effect
        
        // Step 1: Preprocess
        document.getElementById('out-cleaned').textContent = `Cleaned: "${data.cleaned_text}"`;
        steps[0].classList.add('visible');
        
        setTimeout(() => {
            // Step 2: Intent
            document.getElementById('out-intent').textContent = data.intent;
            document.getElementById('out-group').textContent = data.group;
            document.getElementById('out-confidence').textContent = data.confidence;
            steps[1].classList.add('visible');
        }, 600);

        setTimeout(() => {
            // Step 3: RAG
            document.getElementById('out-doc').textContent = data.retrieved_doc_title;
            steps[2].classList.add('visible');
        }, 1200);

        setTimeout(() => {
            // Step 4: LLM
            document.getElementById('out-response').textContent = data.final_response;
            steps[3].classList.add('visible');
            btn.classList.remove('loading');
        }, 1800);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process ticket. Ensure backend is running.');
        btn.classList.remove('loading');
    }
});
