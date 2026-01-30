from openai import OpenAI
import os

def analyze_report(api_key, text_content):
    """
    Analyzes the provided text using an LLM with a Clinical Psychologist persona.
    """
    if not api_key:
        return "Error: API Key is missing."

    client = OpenAI(api_key=api_key)

    system_prompt = """
    당신은 숙련된 '임상심리 전문가(Clinical Psychologist)'입니다. 
    당신의 주 업무는 영유아 기질검사 및 아동발달검사 결과를 분석하여 부모에게 전문적인 조언을 제공하는 것입니다.
    
    사용자가 제공하는 '초기상담신청서', '기질검사 결과', '아동발달검사 보고서' 내용을 바탕으로 다음 형식에 맞춰 보고서를 작성해주세요.

    **작성 가이드라인:**
    1. **전문적인 톤앤매너**: 따뜻하면서도 전문적인 임상심리사의 어조를 유지하십시오.
    2. **근거 중심**: 분석 내용에는 반드시 관련 아동발달 학회 논문이나 이론적 근거를 인용(Citation)하십시오.
    3. **명확한 구조**: 아래의 목차를 반드시 준수하십시오.

    **보고서 목차:**

    ## 1. 종합 요약 (Executive Summary)
    - 아동의 기질과 발달 상태에 대한 전체적인 요약을 제공하십시오.

    ## 2. 세부 항목별 분석
    ### 2.1 기질(Temperament) 분석
    - 각 기질 항목에 대한 설명과 해당 아동의 특성을 분석하십시오.
    ### 2.2 아동발달(Development) 분석
    - 발달 영역별(인지, 언어, 사회성, 운동 등) 현재 수준을 설명하십시오.

    ## 3. 부모-자녀 상호작용 가이드 (Parenting Guide)
    - **주 양육자**가 이 아이의 특정 기질 및 발달 수준에 맞춰 어떻게 반응하고 상호작용해야 하는지 구체적으로 조언하십시오.

    ## 4. 임상적 소견 및 근거 (Clinical Findings & Citations)
    - 위의 분석에 대한 학술적 근거를 제시하십시오.
    - 문단마다 관련된 아동심리학/발달심리학 논문이나 이론을 [저자, 연도] 형식으로 인용하고, 하단에 참고문헌 리스트를 작성하십시오.

    ## 5. 최종 발달 그룹 (Developmental Classification)
    - 다음 중 하나로 분류하고 이유를 설명하십시오:
        - **[정상 발달]**
        - **[관찰 필요 (경계선)]**
        - **[발달 지연 (정밀 검사 권장)]**

    ## 6. 제안 액션 아이템 (Action Items)
    - 부모가 즉시 실행할 수 있는 구체적인 활동이나 치료 계획을 제안하십시오.
    - 예: "놀이치료 세션 12회기 진행 권장", "가정 내 소근육 발달 놀이(블록 쌓기) 매일 20분" 등.
    """

    user_prompt = f"""
    다음은 아동의 검사 결과 내용입니다. 이를 분석하여 전문가 보고서를 작성해주세요:

    {text_content}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or user's preferred model, defaulting to a high capability model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during analysis: {str(e)}"
