--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1 (Debian 16.1-1.pgdg120+1)
-- Dumped by pg_dump version 16.1 (Debian 16.1-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: parktable; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.parktable (
    id integer NOT NULL,
    cid integer,
    region character varying(255),
    park character varying(255),
    vindkraft character varying(255)
);


ALTER TABLE public.parktable OWNER TO admin;

--
-- Name: parktable_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.parktable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parktable_id_seq OWNER TO admin;

--
-- Name: parktable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.parktable_id_seq OWNED BY public.parktable.id;


--
-- Name: parktable id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.parktable ALTER COLUMN id SET DEFAULT nextval('public.parktable_id_seq'::regclass);


--
-- Data for Name: parktable; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.parktable (id, cid, region, park, vindkraft) FROM stdin;
\.


--
-- Name: parktable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.parktable_id_seq', 1, false);


--
-- Name: parktable parktable_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.parktable
    ADD CONSTRAINT parktable_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

