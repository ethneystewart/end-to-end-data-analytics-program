--
-- PostgreSQL database dump
--

\restrict LBufNtn0CvtL6gSC7MPULqtOJsot7ZViMZfd9QNheSJQbb3BwDVVd3heAfaLQMy

-- Dumped from database version 18.3 (Homebrew)
-- Dumped by pg_dump version 18.3 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: mood_type; Type: TYPE; Schema: public; Owner: ethneystewart
--

CREATE TYPE public.mood_type AS ENUM (
    'happy',
    'content',
    'numb',
    'neutral',
    'sad',
    'depressed',
    'anxious',
    'calm',
    'frustrated',
    'angry'
);


ALTER TYPE public.mood_type OWNER TO ethneystewart;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: mood; Type: TABLE; Schema: public; Owner: ethneystewart
--

CREATE TABLE public.mood (
    id integer NOT NULL,
    mood public.mood_type,
    sentiment text,
    moodlog_id integer
);


ALTER TABLE public.mood OWNER TO ethneystewart;

--
-- Name: mood_id_seq; Type: SEQUENCE; Schema: public; Owner: ethneystewart
--

CREATE SEQUENCE public.mood_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mood_id_seq OWNER TO ethneystewart;

--
-- Name: mood_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ethneystewart
--

ALTER SEQUENCE public.mood_id_seq OWNED BY public.mood.id;


--
-- Name: moodlog; Type: TABLE; Schema: public; Owner: ethneystewart
--

CREATE TABLE public.moodlog (
    id integer NOT NULL,
    date date,
    tags text[],
    sleephours integer,
    activities text[],
    energylevel text,
    user_id integer
);


ALTER TABLE public.moodlog OWNER TO ethneystewart;

--
-- Name: moodlog_id_seq; Type: SEQUENCE; Schema: public; Owner: ethneystewart
--

CREATE SEQUENCE public.moodlog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.moodlog_id_seq OWNER TO ethneystewart;

--
-- Name: moodlog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ethneystewart
--

ALTER SEQUENCE public.moodlog_id_seq OWNED BY public.moodlog.id;


--
-- Name: reflection; Type: TABLE; Schema: public; Owner: ethneystewart
--

CREATE TABLE public.reflection (
    id integer NOT NULL,
    reflection text,
    moodlog_id integer
);


ALTER TABLE public.reflection OWNER TO ethneystewart;

--
-- Name: reflection_id_seq; Type: SEQUENCE; Schema: public; Owner: ethneystewart
--

CREATE SEQUENCE public.reflection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reflection_id_seq OWNER TO ethneystewart;

--
-- Name: reflection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ethneystewart
--

ALTER SEQUENCE public.reflection_id_seq OWNED BY public.reflection.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: ethneystewart
--

CREATE TABLE public.users (
    id integer NOT NULL,
    firstname text,
    lastname text,
    email text NOT NULL
);


ALTER TABLE public.users OWNER TO ethneystewart;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: ethneystewart
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO ethneystewart;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ethneystewart
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: mood id; Type: DEFAULT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.mood ALTER COLUMN id SET DEFAULT nextval('public.mood_id_seq'::regclass);


--
-- Name: moodlog id; Type: DEFAULT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.moodlog ALTER COLUMN id SET DEFAULT nextval('public.moodlog_id_seq'::regclass);


--
-- Name: reflection id; Type: DEFAULT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.reflection ALTER COLUMN id SET DEFAULT nextval('public.reflection_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: mood mood_pkey; Type: CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.mood
    ADD CONSTRAINT mood_pkey PRIMARY KEY (id);


--
-- Name: moodlog moodlog_pkey; Type: CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.moodlog
    ADD CONSTRAINT moodlog_pkey PRIMARY KEY (id);


--
-- Name: reflection reflection_pkey; Type: CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.reflection
    ADD CONSTRAINT reflection_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: mood mood_moodlog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.mood
    ADD CONSTRAINT mood_moodlog_id_fkey FOREIGN KEY (moodlog_id) REFERENCES public.moodlog(id);


--
-- Name: moodlog moodlog_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.moodlog
    ADD CONSTRAINT moodlog_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: reflection reflection_moodlog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ethneystewart
--

ALTER TABLE ONLY public.reflection
    ADD CONSTRAINT reflection_moodlog_id_fkey FOREIGN KEY (moodlog_id) REFERENCES public.moodlog(id);


--
-- PostgreSQL database dump complete
--

\unrestrict LBufNtn0CvtL6gSC7MPULqtOJsot7ZViMZfd9QNheSJQbb3BwDVVd3heAfaLQMy

