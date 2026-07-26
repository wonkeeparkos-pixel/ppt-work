# Session tooling state; /home/user/ppt-work/scripts/fetch_papers.py (docstring documenting the same proxy 403 block); curl -sS $HTTPS_PROXY/__agentproxy/status recentRelayFailures

> 이 파일은 원문 PDF가 아니다. 컨테이너 네트워크 정책이 PubMed/PMC/출판사
> 접속을 차단해(프록시 403) 원문을 내려받을 수 없었다. 아래 내용은 문헌검색으로
> 수집한 근거를 문헌 단위로 재조립한 것이며, 초록 원문 전재가 아니다.
> 원문은 아래 링크에서 직접 확인할 것.

## 원문 링크
- [PubMed 검색](https://pubmed.ncbi.nlm.nih.gov/?term=Session+tooling+state;+/home/user/ppt-work/scripts/fetch_papers.py+(docstring+documenting+the+same+proxy+403+block);+cur)

## 이 문헌에서 인용된 근거 (1건)

### [확실] READ THIS FIRST — nothing below was verified against a source in this session; treat every number as a draft to be checked before it goes on a slide.

Hard constraint, not a hedge. (1) WebSearch returned 'this session has used its web search budget (200 of 200 WebSearch calls)' on my first call — zero searches available. (2) WebFetch and curl were refused by the org egress proxy for every relevant host: pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov, www.ncbi.nlm.nih.gov, ebi.ac.uk/europepmc, europepmc.org, painphysicianjournal.com, epain.org, asra.com, spineintervention.org, journals.lww.com, rapm.bmj.com, jamanetwork.com, link.springer.com, onlinelibrary.wiley.com, mdpi.com, api.crossref.org, doi.org, cms.gov, scholar.google.com — all 'CONNECT tunnel failed, response 403'. Proxy README says these are organization policy denials, not to be retried or routed around. (3) The repo's own /home/user/ppt-work/scripts/fetch_papers.py already documents this exact block from a prior session, and the nine topic folders under /home/user/ppt-work/문헌고찰_Lumbar_MBB_Facet/ (including 06_적응증_가이드라인_Guidelines) are empty by design, waiting to be filled on an unblocked network. Consequence: everything that follows is recalled domain knowledge. Author/journal/year are generally reliable; volume/page numbers and especially PMIDs are recalled and MUST be checked; percentages and payer limits are the highest-risk items. Per the task's own rule, a missing fact is fine and a fabricated one is a critical failure — so I have omitted numbers I could not recall cleanly rather than approximating them.

*원 출처 표기*: `Session tooling state; /home/user/ppt-work/scripts/fetch_papers.py (docstring documenting the same proxy 403 block); curl -sS $HTTPS_PROXY/__agentproxy/status recentRelayFailures`
