/*
 * NLE AI Chatbot - Interactive Frontend
 * Professional JavaScript with API Integration
 */

class NLEChatbot {
    constructor() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        this.typingTemplate = document.getElementById('typing-template');
        this.apiResponse = document.getElementById('api-response');

        this.userId = 'user_' + Math.random().toString(36).substr(2, 9);
        this.isTyping = false;
        this.conversationHistory = [];

        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStats();
        this.setupTabs();
        this.setupQuickActions();
        this.setupApiTester();
        this.autoResizeTextarea();
    }

    // ========================
    // Event Bindings
    // ========================
    bindEvents() {
        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Clear chat
        document.getElementById('clear-chat')?.addEventListener('click', () => this.clearChat());

        // Export chat
        document.getElementById('export-chat')?.addEventListener('click', () => this.exportChat());
    }

    // ========================
    // Tab Navigation
    // ========================
    setupTabs() {
        const navBtns = document.querySelectorAll('.nav-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        navBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tabId = btn.dataset.tab;

                // Update active states
                navBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                tabContents.forEach(content => {
                    content.classList.remove('active');
                    if (content.id === `${tabId}-tab`) {
                        content.classList.add('active');
                    }
                });

                // Load stats if stats tab
                if (tabId === 'stats') {
                    this.loadStats();
                }
            });
        });
    }

    // ========================
    // Quick Actions
    // ========================
    setupQuickActions() {
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const message = btn.dataset.message;
                this.messageInput.value = message;
                this.sendMessage();
            });
        });
    }

    // ========================
    // Send Message
    // ========================
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;

        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';

        // Add user message
        this.addMessage(message, 'user');
        this.conversationHistory.push({ role: 'user', content: message, time: new Date() });

        // Show typing indicator
        this.showTyping();
        this.isTyping = true;
        this.sendBtn.disabled = true;

        try {
            // Call API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: this.userId
                })
            });

            const data = await response.json();

            // Hide typing and show response
            this.hideTyping();

            if (data.status === 'success') {
                const botResponse = data.data.response;
                this.addMessage(botResponse, 'bot', data.data);
                this.conversationHistory.push({ 
                    role: 'bot', 
                    content: botResponse, 
                    time: new Date(),
                    intent: data.data.intent,
                    confidence: data.data.confidence
                });
            } else {
                this.addMessage('عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.', 'bot');
            }

        } catch (error) {
            console.error('Error:', error);
            this.hideTyping();
            this.addMessage('⚠️ فشل الاتصال بالخادم. يرجى التحقق من اتصالك.', 'bot');
        } finally {
            this.isTyping = false;
            this.sendBtn.disabled = false;
        }
    }

    // ========================
    // Add Message to Chat
    // ========================
    addMessage(text, sender, metadata = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const time = new Date().toLocaleTimeString('ar-SA', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        // Format text with markdown-like syntax
        let formattedText = this.formatText(text);

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${sender === 'user' ? 'fa-user' : 'fa-robot'}"></i>
            </div>
            <div class="message-content">
                <div class="message-text">${formattedText}</div>
                <span class="message-time">${time}</span>
                ${metadata ? `
                    <span class="message-meta" style="font-size: 10px; color: var(--text-muted); display: block; margin-top: 4px;">
                        ${metadata.intent} • ${(metadata.confidence * 100).toFixed(0)}%
                    </span>
                ` : ''}
            </div>
        `;

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    // ========================
    // Format Text (Markdown-like)
    // ========================
    formatText(text) {
        // Bold: **text**
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--primary-light);">$1</strong>');

        // Code: `text`
        text = text.replace(/`([^`]+)`/g, '<code style="background: var(--bg-hover); padding: 2px 6px; border-radius: 4px; font-family: monospace;">$1</code>');

        // New lines
        text = text.replace(/\n/g, '<br>');

        return text;
    }

    // ========================
    // Typing Indicator
    // ========================
    showTyping() {
        const typingClone = this.typingTemplate.content.cloneNode(true);
        typingClone.querySelector('.typing-message').id = 'typing-indicator';
        this.messagesContainer.appendChild(typingClone);
        this.scrollToBottom();
    }

    hideTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // ========================
    // Scroll to Bottom
    // ========================
    scrollToBottom() {
        this.messagesContainer.scrollTo({
            top: this.messagesContainer.scrollHeight,
            behavior: 'smooth'
        });
    }

    // ========================
    // Clear Chat
    // ========================
    clearChat() {
        if (confirm('هل أنت متأكد من مسح المحادثة؟')) {
            this.messagesContainer.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>تم مسح المحادثة! 🎉</h3>
                    <p>ابدأ محادثة جديدة مع NLE AI</p>
                    <div class="quick-actions">
                        <button class="quick-btn" data-message="مرحبا">
                            <i class="fas fa-hand-wave"></i>
                            <span>تحية</span>
                        </button>
                        <button class="quick-btn" data-message="ما هي قدراتك؟">
                            <i class="fas fa-bolt"></i>
                            <span>القدرات</span>
                        </button>
                        <button class="quick-btn" data-message="ساعدني في البرمجة">
                            <i class="fas fa-code"></i>
                            <span>البرمجة</span>
                        </button>
                        <button class="quick-btn" data-message="احكي لي نكتة">
                            <i class="fas fa-laugh"></i>
                            <span>نكتة</span>
                        </button>
                    </div>
                </div>
            `;
            this.conversationHistory = [];
            this.setupQuickActions();
        }
    }

    // ========================
    // Export Chat
    // ========================
    exportChat() {
        if (this.conversationHistory.length === 0) {
            alert('لا توجد محادثات للتصدير!');
            return;
        }

        let exportText = '🤖 NLE AI Chatbot - Export\n';
        exportText += '='.repeat(50) + '\n\n';

        this.conversationHistory.forEach(msg => {
            const time = msg.time.toLocaleString('ar-SA');
            const role = msg.role === 'user' ? '👤 أنت' : '🤖 NLE AI';
            exportText += `[${time}] ${role}:\n${msg.content}\n\n`;
        });

        const blob = new Blob([exportText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `nle-chat-export-${new Date().toISOString().slice(0,10)}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }

    // ========================
    // Auto-resize Textarea
    // ========================
    autoResizeTextarea() {
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });
    }

    // ========================
    // Load Statistics
    // ========================
    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();

            if (data.status === 'success') {
                const stats = data.data;

                // Update stat cards
                document.getElementById('total-conversations').textContent = stats.total_conversations;
                document.getElementById('unique-users').textContent = stats.unique_users;
                document.getElementById('kb-size').textContent = stats.knowledge_base_size;

                // Update chart
                this.updateIntentChart(stats.intent_distribution, stats.total_conversations);
            }
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }

    // ========================
    // Update Intent Chart
    // ========================
    updateIntentChart(distribution, total) {
        const chartContainer = document.getElementById('intent-chart');
        if (!chartContainer) return;

        chartContainer.innerHTML = '';

        const intentLabels = {
            'greetings': 'التحيات',
            'how_are_you': 'السؤال عن الحال',
            'name': 'الاسم',
            'capabilities': 'القدرات',
            'programming': 'البرمجة',
            'ai_ml': 'الذكاء الاصطناعي',
            'math': 'الرياضيات',
            'weather': 'الطقس',
            'time': 'الوقت',
            'thanks': 'الشكر',
            'goodbye': 'الوداع',
            'joke': 'النكت',
            'insult': 'الإهانات',
            'help': 'المساعدة',
            'default': 'غير معروف'
        };

        const sortedIntents = Object.entries(distribution)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);

        const maxCount = Math.max(...sortedIntents.map(([_, count]) => count));

        sortedIntents.forEach(([intent, count]) => {
            const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;
            const widthPercent = maxCount > 0 ? (count / maxCount * 100) : 0;

            const barItem = document.createElement('div');
            barItem.className = 'chart-bar-item';
            barItem.innerHTML = `
                <div class="chart-bar-label">${intentLabels[intent] || intent}</div>
                <div class="chart-bar-track">
                    <div class="chart-bar-fill" style="width: 0%">
                        <span class="chart-bar-value">${count}</span>
                    </div>
                </div>
            `;

            chartContainer.appendChild(barItem);

            // Animate bar
            setTimeout(() => {
                barItem.querySelector('.chart-bar-fill').style.width = `${Math.max(widthPercent, 5)}%`;
            }, 100);
        });
    }

    // ========================
    // API Tester
    // ========================
    setupApiTester() {
        const testBtn = document.getElementById('test-api-btn');
        if (!testBtn) return;

        testBtn.addEventListener('click', async () => {
            const method = document.getElementById('api-method').value;
            const endpoint = document.getElementById('api-endpoint-input').value;
            const body = document.getElementById('api-body').value;

            testBtn.disabled = true;
            testBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الاختبار...';

            try {
                const options = {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json'
                    }
                };

                if (method === 'POST' && body) {
                    options.body = body;
                }

                const response = await fetch(endpoint, options);
                const data = await response.json();

                this.apiResponse.innerHTML = `<pre><code>${JSON.stringify(data, null, 2)}</code></pre>`;

            } catch (error) {
                this.apiResponse.innerHTML = `<pre><code style="color: var(--danger);">Error: ${error.message}</code></pre>`;
            } finally {
                testBtn.disabled = false;
                testBtn.innerHTML = '<i class="fas fa-play"></i> اختبار';
            }
        });
    }
}

// ========================
// Initialize on DOM Ready
// ========================
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new NLEChatbot();

    // Health check
    fetch('/api/health')
        .then(res => res.json())
        .then(data => {
            console.log('🤖 NLE AI Chatbot Status:', data.status);
            console.log('📡 Service:', data.service);
            console.log('🔧 Version:', data.version);
        })
        .catch(err => console.error('Health check failed:', err));
});
