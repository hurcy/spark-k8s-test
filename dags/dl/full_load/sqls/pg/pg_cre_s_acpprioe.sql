
create table if not exists dkuh_dl.s_acpprioe(
    RPY_PACT_ID varchar(50)
 ,RPY_CLS_SEQ numeric
 ,APY_STR_DT timestamptz
 ,RPY_SEQ numeric
 ,CORG_SEQ numeric
 ,HSP_TP_CD varchar(2)
 ,PT_NO varchar(8)
 ,CORG_CD varchar(4)
 ,CORG_TP_CD varchar(2)
 ,RDTN_RSN_CD varchar(2)
 ,UNCL_RSN_CD varchar(2)
 ,INS_RTO numeric(20,4)
 ,NINS_RTO numeric(20,4)
 ,CMED_RTO numeric(20,4)
 ,CTFS_RTO numeric(20,4)
 ,EXCP_RTO numeric(20,4)
 ,INS_AMT numeric(26,4)
 ,NINS_AMT numeric(26,4)
 ,CMED_AMT numeric(26,4)
 ,CTFS_AMT numeric(26,4)
 ,EXCP_AMT numeric(26,4)
 ,SUM_AMT numeric(26,4)
 ,BOBD_PT_NO varchar(50)
 ,BIND_DTM timestamptz
 ,BIND_STF_NO varchar(6)
 ,RPY_STS_CD varchar(1)
 ,CNCL_DT timestamptz
 ,TOJ_CMED_AMT numeric(26,4)
 ,TOJ_CORG_CMED_RTO numeric(20,4)
 ,FSR_DTM timestamptz
 ,FSR_STF_NO varchar(6)
 ,FSR_PRGM_NM varchar(500)
 ,FSR_IP_ADDR varchar(50)
 ,LSH_DTM timestamptz
 ,LSH_STF_NO varchar(6)
 ,LSH_PRGM_NM varchar(500)
 ,LSH_IP_ADDR varchar(50)
 ,PTHS_CRRT_AMT numeric(26,4)
 ,PTHS_CRRT_RTO numeric(20,4)
 ,GNR_AMT numeric(26,4)
 ,GNR_RTO numeric(20,4)
 ,AMT_APY_YN varchar(1)
 ,MTRL_AMT numeric(20,4)
 ,MTRL_RTO numeric(20,4)
 ,NMC_MTRL_AMT numeric(26,4)
 ,cdw_lod_dtm timestamptz
    , constraint s_acpprioe_pk primary key (RPY_PACT_ID,RPY_CLS_SEQ,APY_STR_DT,RPY_SEQ,CORG_SEQ)
) ;
create index if not exists s_acpprioe_si90 ON dkuh_dl.s_acpprioe USING btree (lsh_dtm);

comment on table dkuh_dl.s_acpprioe is '입원계약기관상세';

comment on column dkuh_dl.s_acpprioe.RPY_PACT_ID is '수납원무접수ID';
comment on column dkuh_dl.s_acpprioe.RPY_CLS_SEQ is '수납유형순번';
comment on column dkuh_dl.s_acpprioe.APY_STR_DT is '적용시작일자';
comment on column dkuh_dl.s_acpprioe.RPY_SEQ is '수납순번';
comment on column dkuh_dl.s_acpprioe.CORG_SEQ is '계약기관순번';
comment on column dkuh_dl.s_acpprioe.HSP_TP_CD is '병원구분코드';
comment on column dkuh_dl.s_acpprioe.PT_NO is '환자번호';
comment on column dkuh_dl.s_acpprioe.CORG_CD is '계약기관코드';
comment on column dkuh_dl.s_acpprioe.CORG_TP_CD is '계약기관구분코드';
comment on column dkuh_dl.s_acpprioe.RDTN_RSN_CD is '감면사유코드';
comment on column dkuh_dl.s_acpprioe.UNCL_RSN_CD is '미수사유코드';
comment on column dkuh_dl.s_acpprioe.INS_RTO is '보험비율';
comment on column dkuh_dl.s_acpprioe.NINS_RTO is '비보험비율';
comment on column dkuh_dl.s_acpprioe.CMED_RTO is '선택진료비율';
comment on column dkuh_dl.s_acpprioe.CTFS_RTO is '제증명비율';
comment on column dkuh_dl.s_acpprioe.EXCP_RTO is '예외비율';
comment on column dkuh_dl.s_acpprioe.INS_AMT is '보험금액';
comment on column dkuh_dl.s_acpprioe.NINS_AMT is '비보험금액';
comment on column dkuh_dl.s_acpprioe.CMED_AMT is '선택진료금액';
comment on column dkuh_dl.s_acpprioe.CTFS_AMT is '제증명금액';
comment on column dkuh_dl.s_acpprioe.EXCP_AMT is '예외금액';
comment on column dkuh_dl.s_acpprioe.SUM_AMT is '합계금액';
comment on column dkuh_dl.s_acpprioe.BOBD_PT_NO is '합본이전환자번호';
comment on column dkuh_dl.s_acpprioe.BIND_DTM is '합본일시';
comment on column dkuh_dl.s_acpprioe.BIND_STF_NO is '합본직원번호';
comment on column dkuh_dl.s_acpprioe.RPY_STS_CD is '수납상태코드';
comment on column dkuh_dl.s_acpprioe.CNCL_DT is '취소일자';
comment on column dkuh_dl.s_acpprioe.TOJ_CMED_AMT is '이관선택진료금액';
comment on column dkuh_dl.s_acpprioe.TOJ_CORG_CMED_RTO is '이관계약기관선택진료비율';
comment on column dkuh_dl.s_acpprioe.FSR_DTM is '최초등록일시';
comment on column dkuh_dl.s_acpprioe.FSR_STF_NO is '최초등록직원번호';
comment on column dkuh_dl.s_acpprioe.FSR_PRGM_NM is '최초등록프로그램명';
comment on column dkuh_dl.s_acpprioe.FSR_IP_ADDR is '최초등록IP주소';
comment on column dkuh_dl.s_acpprioe.LSH_DTM is '최종변경일시';
comment on column dkuh_dl.s_acpprioe.LSH_STF_NO is '최종변경직원번호';
comment on column dkuh_dl.s_acpprioe.LSH_PRGM_NM is '최종변경프로그램명';
comment on column dkuh_dl.s_acpprioe.LSH_IP_ADDR is '최종변경IP주소';
comment on column dkuh_dl.s_acpprioe.PTHS_CRRT_AMT is '보철교정금액';
comment on column dkuh_dl.s_acpprioe.PTHS_CRRT_RTO is '보철교정비율';
comment on column dkuh_dl.s_acpprioe.GNR_AMT is '일반금액';
comment on column dkuh_dl.s_acpprioe.GNR_RTO is '일반비율';
comment on column dkuh_dl.s_acpprioe.AMT_APY_YN is '금액적용여부';
comment on column dkuh_dl.s_acpprioe.MTRL_AMT is '재료금액';
comment on column dkuh_dl.s_acpprioe.MTRL_RTO is '재료비율';
comment on column dkuh_dl.s_acpprioe.NMC_MTRL_AMT is '비급여재료금액';
comment on column dkuh_dl.s_acpprioe.CDW_LOD_DTM is 'CDW 적재 일시';