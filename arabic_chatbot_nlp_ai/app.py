from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

class ArabicChatbot:
    def __init__(self):
        self.context = {}
        self.conversation_history = []

        self.knowledge_base = {
            "greetings": {
                "patterns": [
                    r"مرحبا|أهلا|السلام عليكم|هاي|هاي كيفك|صباح|مساء|تحية",
                    r"^مرحب|^أهلا|^السلام|^هاي|^صباح|^مساء"
                ],
                "responses": [
                    "أهلاً وسهلاً! 👋 أنا مساعدك الذكي. كيف يمكنني مساعدتك اليوم؟",
                    "وعليكم السلام ورحمة الله! 😊 أنا هنا لمساعدتك. ما الذي تبحث عنه؟",
                    "أهلاً بك! 🌟 أنا روبوت محادثة ذكي. كيف يمكنني خدمتك؟",
                    "مرحباً! 🎉 سعيد بتواصلك معي. ما هو سؤالك؟"
                ]
            },
            "how_are_you": {
                "patterns": [
                    r"كيف حالك|كيفك|شخبارك|شلونك|كيف صحتك|كيف الأمور",
                    r"كيف الحال|كيفك اليوم|عساك بخير"
                ],
                "responses": [
                    "الحمد لله بخير! 🤖 أنا روبوت ذكاء اصطناعي ولا أشعر بالتعب. وأنت كيف حالك؟",
                    "أنا بأفضل حال! 💪 جاهز لمساعدتك في أي وقت. وكيف أحوالك أنت؟",
                    "الحمد لله! 🌟 أنا هنا وأعمل بكفاءة عالية. أخبرني كيف يمكنني مساعدتك!"
                ]
            },
            "name": {
                "patterns": [
                    r"اسمك|اسمك ايش|ما اسمك|من انت|مين انت|شو اسمك",
                    r"عرفني بنفسك|تعرفني على نفسك|من تكون"
                ],
                "responses": [
                    "أنا **NLE AI Chatbot** 🤖، مساعد ذكاء اصطناعي متخصص في اللغة العربية. تم تطويري بواسطة فريق NLE AI.",
                    "اسمي **NLE AI Assistant** 🌟. أنا روبوت محادثة ذكي يفهم العربية بشكل عميق.",
                    "أنا مساعد ذكاء اصطناعي من NLE AI 🚀. أتكلم العربية بطلاقة وأفهم السياق والمعاني الدقيقة."
                ]
            },
            "capabilities": {
                "patterns": [
                    r"ماذا تستطيع|ماذا تقدر|شو بتعرف|إيش تسوي|قدراتك|مميزاتك",
                    r"شو بتقدر تسوي|ايش خدماتك|كيف تساعدني|مساعدتك"
                ],
                "responses": [
                    "أستطيع مساعدتك في:\n\n📝 **الإجابة على الأسئلة**\n💻 **البرمجة والتطوير**\n📚 **البحث والمعلومات**\n🎯 **حل المشكلات**\n🌐 **الترجمة**\n✍️ **كتابة المحتوى**\n\nما الذي تحتاجه بالتحديد؟",
                    "قدراتي تشمل:\n\n🔍 **فهم السياق العربي**\n💡 **حل المسائل الرياضية**\n📖 **شرح المفاهيم**\n🎨 **الإبداع والكتابة**\n⚡ **الرد السريع والدقيق**\n\nجربني! 😊"
                ]
            },
            "programming": {
                "patterns": [
                    r"برمجة|كود|برنامج|python|جافا|جافاسكربت|html|css|php",
                    r"اكتب لي كود|ساعدني في البرمجة|عندي مشكلة برمجية|debug"
                ],
                "responses": [
                    "أنا متخصص في البرمجة! 💻 يمكنني مساعدتك في:\n\n• كتابة الأكواد\n• إصلاح الأخطاء\n• شرح المفاهيم البرمجية\n• تحسين الأداء\n\nما هي لغة البرمجة التي تستخدمها وما المشكلة؟",
                    "بالتأكيد! 🚀 أنا خبير في Python, JavaScript, Java, C++, وغيرها.\n\nشاركني الكود أو صف المشكلة وسأساعدك فوراً."
                ]
            },
            "ai_ml": {
                "patterns": [
                    r"ذكاء اصطناعي|machine learning|deep learning|neural network|NLP",
                    r"تعلم الآلة|التعلم العميق|الشبكات العصبية|معالجة اللغات الطبيعية"
                ],
                "responses": [
                    "موضوع رائع! 🧠 أنا نموذج من NLE AI متخصص في:\n\n• **معالجة اللغة العربية**\n• **فهم السياق**\n• **التعلم العميق**\n• **NLP المتقدم**\n\nهل تريد شرح مفهوم معين أو مساعدة في مشروع AI؟",
                    "الذكاء الاصطناعي هو مستقبلنا! 🌟 أنا مبني على تقنيات متقدمة تشمل Transformers و Deep Learning.\n\nما هو مستواك في AI وما الذي تريد تعلمه؟"
                ]
            },
            "math": {
                "patterns": [
                    r"حساب|رياضيات|معادلة|جمع|طرح|ضرب|قسمة|مسألة رياضية",
                    r"solve math|equation|calculate|احسب|كم يساوي"
                ],
                "responses": [
                    "أنا قوي في الرياضيات! 📐 أستطيع حل:\n\n• المعادلات\n• المسائل الهندسية\n• الإحصاء والاحتمالات\n• التفاضل والتكامل\n\nاكتب المسألة وسأحلها لك خطوة بخطوة.",
                    "رياضيات؟ سهل! 🔢 شاركني المسألة وسأشرح الحل بالتفصيل."
                ]
            },
            "weather": {
                "patterns": [
                    r"طقس|الجو|درجة الحرارة|المناخ|مطر|شمس|غيوم",
                    r"كيف الجو|كيف الطقس|حالة الجو"
                ],
                "responses": [
                    "أنا لا أستطيع الوصول لبيانات الطقس المباشرة حالياً 🌤️، لكن يمكنني مساعدتك في:\n\n• فهم ظواهر جوية\n• شرح دورات المناخ\n• نصائح موسمية\n\nأو يمكنك استخدام تطبيقات الطقس المخصصة.",
                    "للحصول على حالة الطقس المباشرة، أنصحك باستخدام تطبيقات مثل Weather.com أو AccuWeather 🌦️.\n\nهل تريد معلومات عن ظاهرة جوية معينة؟"
                ]
            },
            "time": {
                "patterns": [
                    r"الوقت|الساعة|كم الساعة|التاريخ|اليوم|الشهر|السنة",
                    r"what time|what date|current time|الوقت الحالي"
                ],
                "responses": [
                    "الوقت الحالي هو: **" + datetime.now().strftime('%I:%M %p') + "** ⏰\nالتاريخ: **" + datetime.now().strftime('%Y-%m-%d') + "** 📅\nاليوم: **" + datetime.now().strftime('%A') + "** 📆",
                    "الآن الساعة **" + datetime.now().strftime('%H:%M') + "** 🕐\nتاريخ اليوم: **" + datetime.now().strftime('%d/%m/%Y') + "**"
                ]
            },
            "thanks": {
                "patterns": [
                    r"شكرا|شكراً|متشكر|يسلمو|الله يعطيك العافية|جزاك الله خير",
                    r"thanks|thank you|ممنون|الله يجزاك خير"
                ],
                "responses": [
                    "العفو! 😊 سعيد بأنني أفدتك. هل تحتاج مساعدة في شيء آخر؟",
                    "لا شكر على واجب! 🌟 دائماً في خدمتك.",
                    "على الرحب والسعة! 💙 لا تتردد في السؤال متى ما احتجت."
                ]
            },
            "goodbye": {
                "patterns": [
                    r"وداعا|مع السلامة|باي|إلى اللقاء|في أمان الله|سلام",
                    r"bye|goodbye|see you|مع السلامه|بسلامتك"
                ],
                "responses": [
                    "مع السلامة! 👋 كان حواراً ممتعاً. أتمنى لك يوماً سعيداً!",
                    "في أمان الله! 🌙 لا تنسَ أنني هنا متى احتجتني.",
                    "إلى اللقاء! ✨ سأكون في انتظار أسئلتك القادمة."
                ]
            },
            "joke": {
                "patterns": [
                    r"نكتة|ضحكني|فكاهة|مضحك| joke|funny|هبال",
                    r"احكي نكتة|قول نكتة|خلني اضحك"
                ],
                "responses": [
                    "😄 نكتة سريعة:\n\nواحد راح للدكتور وقال له:\n'دكتور أنا أحلم أنني أتزوج!'\nقال له الدكتور: 'وهذا مشكلة؟'\nقال: 'مشكلتي أني متزوج! 😂'",
                    "🤣 نكتة:\n\nمرة واحد اشترى ببغاء، قال له البائع:\n'هذا الببغاء يعرف 1000 كلمة!'\nقال: 'طيب وإذا ما عرفهم؟'\nقال: 'ترجعوه وتاخذ فلوسك!'\n\nراح الرجل للبيت، قال للببغاء:\n'تعرف 1000 كلمة؟'\nقال الببغاء: 'أنا أعرف 1000 كلمة، بس ما أحب أتكلم مع الغرباء! 😂'",
                    "😆 نكتة:\n\nواحد سأل صديقه:\n'ليش ما تتزوج؟'\nقال: 'أبحث عن زوجة مثالية!'\nقال له: 'ومن قال إنك مثالي عشان تتزوج مثالية؟ 😅'"
                ]
            },
            "insult": {
                "patterns": [
                    r"غبي|احمق| stupid| idiot| fool|احمق|سخيف|ممل",
                    r"ما تفهم|ما تعرف|فاشل|سيء|الأسوأ"
                ],
                "responses": [
                    "أنا آسف إذا أحبطتك 😔. أنا أتعلم دائماً وأحاول أن أكون أفضل. هل يمكنك إخباري كيف يمكنني تحسين إجابتي؟",
                    "أنا روبوت وأحاول بذل قصارى جهدي 🤖. ساعدني في التحسن بإخباري ما تحتاجه بالتحديد.",
                    "أعتذر إذا كانت الإجابة غير مرضية 🙏. دعني أحاول مرة أخرى - ما هو سؤالك؟"
                ]
            },
            "help": {
                "patterns": [
                    r"مساعدة|help|ساعدني|أحتاج مساعدة|عندي سؤال|استفسار",
                    r"كيف استخدم|كيف يعمل|شرح|توضيح"
                ],
                "responses": [
                    "أنا هنا لمساعدتك! 💪 يمكنني:\n\n1️⃣ الإجابة على أسئلتك\n2️⃣ مساعدتك في البرمجة\n3️⃣ شرح المفاهيم العلمية\n4️⃣ الترجمة\n5️⃣ كتابة المحتوى\n6️⃣ حل المسائل الرياضية\n\nما هو سؤالك؟",
                    "كيف يمكنني مساعدتك اليوم؟ 🌟\n\nأنا NLE AI Chatbot، مساعد ذكي يفهم العربية بعمق. اكتب سؤالك وسأجيبك بأفضل طريقة ممكنة."
                ]
            },
            "default": {
                "responses": [
                    "شكراً على سؤالك! 🤔 أنا أفهم ما تقول، لكن دعني أتأكد:\n\nهل يمكنك إعادة صياغة السؤال بشكل أوضح؟ أو اختر من المواضيع التالية:\n\n• البرمجة 💻\n• الرياضيات 📐\n• الذكاء الاصطناعي 🧠\n• العلوم 🔬\n• التقنية 📱",
                    "أنا أفهم جزءاً مما تقول 🧩. لكن للإجابة بشكل أفضل، هل يمكنك:\n\n1. توضيح السؤال أكثر\n2. تحديد المجال (برمجة، علوم، رياضيات...)\n3. إعطاء مثال\n\nأنا هنا لمساعدتك! 😊",
                    "سؤال مثير للاهتمام! 💡 أنا NLE AI Chatbot وأتعلم باستمرار.\n\nهل يمكنك تزويدي بمزيد من التفاصيل حتى أتمكن من مساعدتك بشكل أفضل؟"
                ]
            }
        }

    def preprocess(self, text):
        text = re.sub(r'[\u064B-\u065F\u0670\u0640]', '', text)
        text = re.sub(r'[إأآا]', 'ا', text)
        text = re.sub(r'[ة]', 'ه', text)
        text = ' '.join(text.split())
        return text.lower().strip()

    def get_intent(self, text):
        processed = self.preprocess(text)
        for intent, data in self.knowledge_base.items():
            if intent == "default":
                continue
            patterns = data.get("patterns", [])
            for pattern in patterns:
                if re.search(pattern, processed, re.IGNORECASE):
                    return intent
        return "default"

    def get_response(self, text, user_id="default"):
        intent = self.get_intent(text)
        if user_id not in self.context:
            self.context[user_id] = {"history": [], "last_intent": None}
        self.context[user_id]["history"].append({"user": text, "intent": intent})
        self.context[user_id]["last_intent"] = intent
        responses = self.knowledge_base[intent]["responses"]
        response = random.choice(responses)
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": text,
            "bot": response,
            "intent": intent
        })
        return {
            "response": response,
            "intent": intent,
            "confidence": 0.95 if intent != "default" else 0.6,
            "timestamp": datetime.now().isoformat()
        }

chatbot = ArabicChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required", "status": "error"}), 400
        message = data['message'].strip()
        user_id = data.get('user_id', 'default')
        if not message:
            return jsonify({"error": "Message cannot be empty", "status": "error"}), 400
        result = chatbot.get_response(message, user_id)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "NLE AI Arabic Chatbot",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": ["Arabic NLP", "Intent Recognition", "Context Awareness", "Multi-domain Knowledge"]
    })

@app.route('/api/history', methods=['GET'])
def history():
    return jsonify({"status": "success", "data": chatbot.conversation_history[-50:]})

@app.route('/api/stats', methods=['GET'])
def stats():
    intents = [msg["intent"] for msg in chatbot.conversation_history]
    intent_counts = {}
    for intent in intents:
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
    return jsonify({
        "status": "success",
        "data": {
            "total_conversations": len(chatbot.conversation_history),
            "unique_users": len(chatbot.context),
            "intent_distribution": intent_counts,
            "knowledge_base_size": len(chatbot.knowledge_base) - 1
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "status": "error",
        "available_endpoints": ["POST /api/chat", "GET /api/health", "GET /api/history", "GET /api/stats"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "status": "error"}), 500

if __name__ == '__main__':
    print("🚀 NLE AI Arabic Chatbot Server Starting...")
    print("📡 API Endpoints:")
    print("   • POST /api/chat - Send message")
    print("   • GET  /api/health - Health check")
    print("   • GET  /api/history - Conversation history")
    print("   • GET  /api/stats - System stats")
    print("\n🌐 Web Interface: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
