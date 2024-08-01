import re
templates_full_data = {
    # 正面
    "template_1": ["Noted for its {Opinion}, the {Aspect} of the {Category} indicates a {Sentiment} perspective.",
                   "Indicating a {Sentiment} perspective, the {Aspect} of the {Category} was noted as {Opinion}."],
    # 对比描述
    "template_2": ["Giving a {Sentiment} conclusion, the {Aspect} related to the {Category} seemed {Opinion}.",
                   "The {Category} had a {Sentiment} conclusion, as the {Aspect} related to it seemed {Opinion}."],
    # 因果描述
    "template_3": ["There's a resulting {Sentiment} sentiment because the {Aspect} in the {Category} is {Opinion}.",
                   "A resulting {Sentiment} sentiment is observed because the {Aspect} in {Category} is {Opinion}."],
    # 上下文背景
    "template_4": ["Which was {Opinion}, given the {Aspect} in the {Category}, the overall sentiment was {Sentiment}."],
    # 陈述事实
    "template_5": ["Resulting in {Sentiment} sentiment, it was found that the {Aspect} of the {Category} is {Opinion}.",
                   "The {Aspect} of the {Category} is {Opinion}, which was found to result in {Sentiment} sentiment."],
    # 建议
    "template_6": ["The expected sentiment is {Sentiment}, given that the {Aspect} in the {Category} is about {Opinion}.",
                   "Given that the {Aspect} in {Category} is {Opinion}, the sentiment expected is {Sentiment}."],
    # 叙述
    "template_7": ["It was noted as {Opinion}, analyzing the {Aspect} of the {Category}, leading to a {Sentiment} sentiment.",
                    "Leading to a {Sentiment} sentiment, analyzing the {Aspect} of {Category}, it was noted as {Opinion}."]
}

instruction = '''
You are an advanced artificial intelligence model specifically designed to identify sentiment attribute tuples in text.
First, you are provided with some categories, including ## .

Instructions:
Carefully read the provided text and identify the sentiment tuples that appear in the text, give the consideration process and return each extraction result in the order of [Aspect, Category, Opinion, Sentiment].

Aspect refers to the specific feature or aspect being evaluated in the text. When it does not appear in the text, return NULL. 
Category is the process of categorizing or classifying the aspects identified in the text for better analysis and organization of the sentiment information.
Opinion refers to the author's or reviewer's specific evaluation or viewpoint on a particular aspect. 
Sentiment denotes the specific emotional state or tendency expressed in the text, which can be positive, negative, or neutral. 
If there are no identifiable sentiment attribute tuples in the text, return an empty list.

Input format: Text data.
Output format: A text containing consideration process and extraction results. 
If there are more than one result, the consideration process of each are split by [sep]. 

Example:
Input text: The ambience was so fun , and the prices were great , on top of the fact that the food was really tasty. 
Output :  [sep] Noted for its fun, the ambience of the ambience general indicates a positive perspective. 
[sep] Noted for its great, the one of the restaurant prices indicates a positive perspective. 
[sep] Noted for its tasty, the food of the food quality indicates a positive perspective.
So the result of the prediction is [['ambience', 'ambience general', 'positive', 'fun'], 
['NULL', 'restaurant prices', 'positive', 'great'], ['food', 'food quality', 'positive', 'tasty']]

Special notes:
The identified Category must be one of the predefined ones, and the Sentiment must be positive, negative, or neutral.
For ambiguous or potentially ambiguous tuples, do not output.
Focus on the extraction of sentiment tuples without summarizing or interpreting the text.

Here is the input data, please provide the output result:
'''.replace("\n", "")






instruction_for_cot = '''
You are currently executing a task of @@. You are an advanced artificial intelligence model specifically designed to identify sentiment attribute tuples in text.
First, you are provided with some categories, including ## .

Instructions:
Carefully read the provided text and identify the sentiment tuples that appear in the text, return the consideration process.

Aspect refers to the specific feature or aspect being evaluated in the text. 
Category is the process of categorizing or classifying the aspects identified in the text for better analysis and organization of the sentiment information.
Opinion refers to the author's or reviewer's specific evaluation or viewpoint on a particular aspect. 
Sentiment denotes the specific emotional state or tendency expressed in the text, which can be positive, negative, or neutral. 

Input format: Template order and text data.
Output format: A text containing template order and consideration process. 
If there are no aspect terms or opinion, replace it by one.
If there are more than one result, the consideration process of each are split by [sep]. 

Example: 
Input text: [Template_1] The ambience was so fun , and the prices were great , on top of the fact that the food was really tasty. 
Output :  [Template_1] [sep] Noted for its fun, the ambience of the ambience general indicates a positive perspective. 
[sep] Noted for its great, the one of the restaurant prices indicates a positive perspective. 
[sep] Noted for its tasty, the food of the food quality indicates a positive perspective.

Special notes: 
The identified Category must be one of the predefined ones, and the Sentiment must be positive, negative, or neutral.
For ambiguous or potentially ambiguous tuples, do not output.
Focus on the extraction of sentiment tuples without summarizing or interpreting the text.

Here is the input data, please provide the output result:
'''.replace("\n", "")


instruction_for_cot_ASTE = '''
You are currently executing a task of @@. You are an advanced artificial intelligence model specifically designed to identify sentiment attribute tuples in text.

Instructions:
Carefully read the provided text and identify the sentiment tuples that appear in the text, return the consideration process.

Aspect refers to the specific feature or aspect being evaluated in the text. 
Opinion refers to the author's or reviewer's specific evaluation or viewpoint on a particular aspect. 
Sentiment denotes the specific emotional state or tendency expressed in the text, which can be positive, negative, or neutral. 

Input format: Template order and text data.
Output format: A text containing template order and consideration process. 
If there are more than one result, the consideration process of each are split by [sep]. 

Example: 
Input text: [Template_1] In the shop , these MacBooks are encased in a soft rubber enclosure - so you will never know about the razor edge until you buy it , get it home , break the seal and use it ( very clever con ) .
Output :  [Template_1] [sep] Noted for its soft, the rubber enclosure of the text indicates a positive perspective.

Special notes: 
Sentiment must be positive, negative, or neutral.
For ambiguous or potentially ambiguous tuples, do not output.
Focus on the extraction of sentiment tuples without summarizing or interpreting the text.

Here is the input data, please provide the output result:
'''.replace("\n", "")

instruction_for_cot_TASD = '''
You are currently executing a task of @@. You are an advanced artificial intelligence model specifically designed to identify sentiment attribute tuples in text.
First, you are provided with some categories, including ## .

Instructions:
Carefully read the provided text and identify the sentiment tuples that appear in the text, return the consideration process.

Aspect refers to the specific feature or aspect being evaluated in the text. 
Category is the process of categorizing or classifying the aspects identified in the text for better analysis and organization of the sentiment information. 
Sentiment denotes the specific emotional state or tendency expressed in the text, which can be positive, negative, or neutral. 

Input format: Template order and text data.
Output format: A text containing template order and consideration process. 
If there are more than one result, the consideration process of each are split by [sep]. 

Example: 
Input text: [Template_1] Judging from previous posts this used to be a good place , but not any longer .
Output: [Template_1] [sep] Noted for its natural, the place of the restaurant general indicates a negative perspective

Special notes: 
The identified Category must be one of the predefined ones, and the Sentiment must be positive, negative, or neutral.
For ambiguous or potentially ambiguous tuples, do not output.
Focus on the extraction of sentiment tuples without summarizing or interpreting the text.

Here is the input data, please provide the output result:
'''.replace("\n", "")

templates_full_data_TASD = {
    # 正面
    "template_1": ["Noted for its natural, the {Aspect} of the {Category} indicates a {Sentiment} perspective.",
                   "Indicating a {Sentiment} perspective, the {Aspect} of the {Category} was noted as significant."],
    # 对比描述
    "template_2": ["Giving a {Sentiment} conclusion, the {Aspect} related to the {Category} seemed natural.",
                   "The {Category} had a {Sentient} conclusion, as the {Aspect} related to it seemed evident."],
    # 因果描述
    "template_3": ["There's a resulting {Sentiment} sentiment because the {Aspect} in the {Category} is natural.",
                   "A resulting {Sentiment} sentiment is observed because the {Aspect} in {Category} is noteworthy."],
    # 上下文背景
    "template_4": ["Which was natural, given the {Aspect} in the {Category}, the overall sentiment was {Sentiment}."],
    # 陈述事实
    "template_5": ["Resulting in {Sentiment} sentiment, it was found that the {Aspect} of the {Category} is natural.",
                   "The {Aspect} of the {Category} is pivotal, which was found to result in {Sentiment} sentiment."],
    # 建议
    "template_6": ["The expected sentiment is {Sentiment}, given that the {Aspect} in the {Category} is about natural.",
                   "Given that the {Aspect} in {Category} is core, the sentiment expected is {Sentiment}."],
    # 叙述
    "template_7": ["It was noted as natural, analyzing the {Aspect} of the {Category}, leading to a {Sentiment} sentiment.",
                    "Leading to a {Sentiment} sentiment, analyzing the {Aspect} of {Category}, it was noted as critical."]
}


templates_full_data_ASTE = {
    # 正面
    "template_1": ["Noted for its {Opinion}, the {Aspect} of the text indicates a {Sentiment} perspective.",
                   "Indicating a {Sentiment} perspective, the {Aspect} of the {Category} was noted as {Opinion}."],
    # 对比描述
    "template_2": ["Giving a {Sentiment} conclusion, the {Aspect} related to the text seemed {Opinion}.",
                   "The {Category} had a {Sentiment} conclusion, as the {Aspect} related to it seemed {Opinion}."],
    # 因果描述
    "template_3": ["There's a resulting {Sentiment} sentiment because the {Aspect} in the text is {Opinion}.",
                   "A resulting {Sentiment} sentiment is observed because the {Aspect} in {Category} is {Opinion}."],
    # 上下文背景
    "template_4": ["Which was {Opinion}, given the {Aspect} in the text, the overall sentiment was {Sentiment}."],
    # 陈述事实
    "template_5": ["Resulting in {Sentiment} sentiment, it was found that the {Aspect} of the text is {Opinion}.",
                   "The {Aspect} of the {Category} is {Opinion}, which was found to result in {Sentiment} sentiment."],
    # 建议
    "template_6": ["The expected sentiment is {Sentiment}, given that the {Aspect} in the text is about {Opinion}.",
                   "Given that the {Aspect} in {Category} is {Opinion}, the sentiment expected is {Sentiment}."],
    # 叙述
    "template_7": ["It was noted as {Opinion}, analyzing the {Aspect} of the text, leading to a {Sentiment} sentiment.",
                    "Leading to a {Sentiment} sentiment, analyzing the {Aspect} of {Category}, it was noted as {Opinion}."]
}


def get_parser(template):
    if template == "Template_1:" or template == "[Template_1]":
        opinion_pattern = re.compile(r'Noted for its (.*?),')
        aspect_pattern = re.compile(r'the (.*?) of the')
        entity_pattern = re.compile(r'of the (.*?) indicate')
        perspective_pattern = re.compile(r'indicates a (.*) perspective')
        return aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern

    if template == "Template_2:" or template == "[Template_2]":
        opinion_pattern  = re.compile(r'seemed (.*?)\.')
        aspect_pattern = re.compile(r'the (.*?) related to')
        entity_pattern = re.compile(r'to the (.*?) seemed')
        perspective_pattern = re.compile(r'Giving a (.*?) conclusion')
        return aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern

    if template == "Template_3:" or template == "[Template_3]":
        aspect_pattern = re.compile(r'because the (.*?) in')
        opinion_pattern = re.compile(r'is (.*?)\.')
        entity_pattern = re.compile(r'in the (.*?) is')
        perspective_pattern = re.compile(r's a resulting (.*?) sentiment')
        return aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern

    if template == "Template_4:" or template == "[Template_4]":
        aspect_pattern = re.compile(r'given the (.*?) in')
        opinion_pattern = re.compile(r'Which was (.*?),')
        entity_pattern = re.compile(r'in the (.*?),')
        perspective_pattern = re.compile(r'the overall sentiment was (.*?)\.')
        return aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern

    if template == "Template_5:" or template == "[Template_5]":
        aspect_pattern = re.compile(r'it was found that the (.*?) of the')
        opinion_pattern = re.compile(r'is (.*?)\.')
        entity_pattern = re.compile(r'of the (.*?) is')
        perspective_pattern = re.compile(r'Resulting in (.*?) sentiment')
        return aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern

    if template == "Template_6:" or template == "[Template_6]":
        aspect_pattern = re.compile(r'given that the (.*?) in')
        opinion_pattern = re.compile(r'is about (.*?)\.')
        entity_pattern = re.compile(r'in the (.*?) is')
        perspective_pattern = re.compile(r'The expected sentiment is (.*?),')
        return aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern

    if template == "Template_7:" or template == "[Template_7]":
        aspect_pattern = re.compile(r'analyzing the (.*?) of')
        opinion_pattern = re.compile(r'It was noted as (.*?),')
        entity_pattern = re.compile(r'of the (.*?),')
        perspective_pattern = re.compile(r'leading to a (.*?) sentiment\.')
        return aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern




laptop_aspect_cate_list = [
    'keyboard operation_performance', 'os operation_performance',
    'out_of_scope operation_performance', 'ports general',
    'optical_drives general', 'laptop operation_performance',
    'optical_drives operation_performance', 'optical_drives usability',
    'multimedia_devices general', 'keyboard general', 'os miscellaneous',
    'software operation_performance', 'display operation_performance',
    'shipping quality', 'hard_disc quality', 'motherboard general',
    'graphics general', 'multimedia_devices connectivity', 'display general',
    'memory operation_performance', 'os design_features',
    'out_of_scope usability', 'software design_features',
    'graphics design_features', 'ports connectivity',
    'support design_features', 'display quality', 'software price',
    'shipping general', 'graphics operation_performance',
    'hard_disc miscellaneous', 'display design_features',
    'cpu operation_performance', 'mouse general', 'keyboard portability',
    'hardware price', 'support quality', 'hardware quality',
    'motherboard operation_performance', 'multimedia_devices quality',
    'battery design_features', 'mouse usability', 'os price',
    'shipping operation_performance', 'laptop quality', 'laptop portability',
    'fans&cooling general', 'battery general', 'os usability',
    'hardware usability', 'optical_drives design_features',
    'fans&cooling operation_performance', 'memory general', 'company general',
    'power_supply general', 'hardware general', 'mouse design_features',
    'software general', 'keyboard quality', 'power_supply quality',
    'software quality', 'multimedia_devices usability',
    'power_supply connectivity', 'multimedia_devices price',
    'multimedia_devices operation_performance', 'ports design_features',
    'hardware operation_performance', 'shipping price',
    'hardware design_features', 'memory usability', 'cpu quality',
    'ports quality', 'ports portability', 'motherboard quality',
    'display price', 'os quality', 'graphics usability', 'cpu design_features',
    'hard_disc general', 'hard_disc operation_performance', 'battery quality',
    'laptop usability', 'company design_features',
    'company operation_performance', 'support general', 'fans&cooling quality',
    'memory design_features', 'ports usability', 'hard_disc design_features',
    'power_supply design_features', 'keyboard miscellaneous',
    'laptop miscellaneous', 'keyboard usability', 'cpu price',
    'laptop design_features', 'keyboard price', 'warranty quality',
    'display usability', 'support price', 'cpu general',
    'out_of_scope design_features', 'out_of_scope general',
    'software usability', 'laptop general', 'warranty general',
    'company price', 'ports operation_performance',
    'power_supply operation_performance', 'keyboard design_features',
    'support operation_performance', 'hard_disc usability', 'os general',
    'company quality', 'memory quality', 'software portability',
    'fans&cooling design_features', 'multimedia_devices design_features',
    'laptop connectivity', 'battery operation_performance', 'hard_disc price',
    'laptop price'
]

rest_aspect_cate_list = [
    'location general', 'food prices', 'food quality', 'food general',
    'ambience general', 'service general', 'restaurant prices',
    'drinks prices', 'restaurant miscellaneous', 'drinks quality',
    'drinks style_options', 'restaurant general', 'food style_options'
]
