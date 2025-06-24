--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Ubuntu 17.5-1.pgdg22.04+1)
-- Dumped by pg_dump version 17.5 (Ubuntu 17.5-1.pgdg22.04+1)

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
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: antond
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.django_content_type VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type VALUES (3, 'auth', 'group');
INSERT INTO public.django_content_type VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type VALUES (5, 'sessions', 'session');
INSERT INTO public.django_content_type VALUES (6, 'store', 'category');
INSERT INTO public.django_content_type VALUES (7, 'store', 'ingredient');
INSERT INTO public.django_content_type VALUES (8, 'store', 'order');
INSERT INTO public.django_content_type VALUES (9, 'store', 'orderitem');
INSERT INTO public.django_content_type VALUES (10, 'userprofile', 'user');
INSERT INTO public.django_content_type VALUES (11, 'userprofile', 'userprofile');
INSERT INTO public.django_content_type VALUES (12, 'token_blacklist', 'blacklistedtoken');
INSERT INTO public.django_content_type VALUES (13, 'token_blacklist', 'outstandingtoken');


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.auth_permission VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO public.auth_permission VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO public.auth_permission VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO public.auth_permission VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO public.auth_permission VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission VALUES (21, 'Can add Category', 6, 'add_category');
INSERT INTO public.auth_permission VALUES (22, 'Can change Category', 6, 'change_category');
INSERT INTO public.auth_permission VALUES (23, 'Can delete Category', 6, 'delete_category');
INSERT INTO public.auth_permission VALUES (24, 'Can view Category', 6, 'view_category');
INSERT INTO public.auth_permission VALUES (25, 'Can add Ingredient', 7, 'add_ingredient');
INSERT INTO public.auth_permission VALUES (26, 'Can change Ingredient', 7, 'change_ingredient');
INSERT INTO public.auth_permission VALUES (27, 'Can delete Ingredient', 7, 'delete_ingredient');
INSERT INTO public.auth_permission VALUES (28, 'Can view Ingredient', 7, 'view_ingredient');
INSERT INTO public.auth_permission VALUES (29, 'Can add order', 8, 'add_order');
INSERT INTO public.auth_permission VALUES (30, 'Can change order', 8, 'change_order');
INSERT INTO public.auth_permission VALUES (31, 'Can delete order', 8, 'delete_order');
INSERT INTO public.auth_permission VALUES (32, 'Can view order', 8, 'view_order');
INSERT INTO public.auth_permission VALUES (33, 'Can add order item', 9, 'add_orderitem');
INSERT INTO public.auth_permission VALUES (34, 'Can change order item', 9, 'change_orderitem');
INSERT INTO public.auth_permission VALUES (35, 'Can delete order item', 9, 'delete_orderitem');
INSERT INTO public.auth_permission VALUES (36, 'Can view order item', 9, 'view_orderitem');
INSERT INTO public.auth_permission VALUES (37, 'Can add user', 10, 'add_user');
INSERT INTO public.auth_permission VALUES (38, 'Can change user', 10, 'change_user');
INSERT INTO public.auth_permission VALUES (39, 'Can delete user', 10, 'delete_user');
INSERT INTO public.auth_permission VALUES (40, 'Can view user', 10, 'view_user');
INSERT INTO public.auth_permission VALUES (41, 'Can add user profile', 11, 'add_userprofile');
INSERT INTO public.auth_permission VALUES (42, 'Can change user profile', 11, 'change_userprofile');
INSERT INTO public.auth_permission VALUES (43, 'Can delete user profile', 11, 'delete_userprofile');
INSERT INTO public.auth_permission VALUES (44, 'Can view user profile', 11, 'view_userprofile');
INSERT INTO public.auth_permission VALUES (45, 'Can add blacklisted token', 12, 'add_blacklistedtoken');
INSERT INTO public.auth_permission VALUES (46, 'Can change blacklisted token', 12, 'change_blacklistedtoken');
INSERT INTO public.auth_permission VALUES (47, 'Can delete blacklisted token', 12, 'delete_blacklistedtoken');
INSERT INTO public.auth_permission VALUES (48, 'Can view blacklisted token', 12, 'view_blacklistedtoken');
INSERT INTO public.auth_permission VALUES (49, 'Can add outstanding token', 13, 'add_outstandingtoken');
INSERT INTO public.auth_permission VALUES (50, 'Can change outstanding token', 13, 'change_outstandingtoken');
INSERT INTO public.auth_permission VALUES (51, 'Can delete outstanding token', 13, 'delete_outstandingtoken');
INSERT INTO public.auth_permission VALUES (52, 'Can view outstanding token', 13, 'view_outstandingtoken');


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: antond
--



--
-- Data for Name: userprofile_user; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.userprofile_user VALUES (1, 'pbkdf2_sha256$600000$eFQaZ6cJ2RWzQ3mxiyqUCB$x/BAe8GXjnR0FtQgFmHt6PXAPP+EJvbrsH4lLr7Tt5s=', '2025-06-16 13:55:21.458313+03', true, '', '', true, true, '2025-05-28 19:25:28.18216+03', 'admin', 'admin@gmail.com', NULL);
INSERT INTO public.userprofile_user VALUES (2, 'pbkdf2_sha256$600000$5LTAuNvYtrXrU2DfsvnBrK$3KyYwwU/yACGeJMSPG0VDCX4EjE42likJ4fggfbfQ/8=', '2025-06-09 22:52:41.596696+03', false, '', '', false, true, '2025-06-02 17:28:12.32485+03', 'AntonTheMighty', 'doublescreen509@gmail.com', NULL);
INSERT INTO public.userprofile_user VALUES (13, 'pbkdf2_sha256$600000$wZXoe7WFhcpXHuNrvYOxVO$H1GThviWxy53bpFa6CZKS0BD2TIOxxRG1JrD3bvonN8=', '2025-06-19 11:37:37.403521+03', false, '', '', false, true, '2025-06-16 12:55:30.921909+03', 'dizain-mebli@ukr.net', 'dizain-mebli@ukr.net', '2025-06-17 16:12:26.488237+03');


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.django_admin_log VALUES (1, '2025-05-28 19:26:06.422848+03', '1', 'Emollients', 1, '[{"added": {}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (2, '2025-05-28 19:26:13.200103+03', '2', 'Surfactants', 1, '[{"added": {}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (3, '2025-05-28 19:26:18.355799+03', '3', 'Dyes', 1, '[{"added": {}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (4, '2025-05-28 20:02:12.618362+03', '1', 'Sodium Lauryl Sulfate', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log VALUES (5, '2025-05-28 20:03:31.723235+03', '2', 'Cetyl Alcohol', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log VALUES (6, '2025-05-28 20:17:43.662734+03', '3', 'Amodimethicone', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log VALUES (7, '2025-05-28 20:18:33.009063+03', '4', 'Ethylhexyl Olivate', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log VALUES (8, '2025-05-28 20:20:49.775119+03', '5', 'Beetroot Extract', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log VALUES (41, '2025-06-02 10:42:22.994787+03', '5', 'Beetroot Extract', 2, '[{"changed": {"fields": ["Quantity"]}}]', 7, 1);
INSERT INTO public.django_admin_log VALUES (42, '2025-06-02 10:42:32.065779+03', '4', 'Ethylhexyl Olivate', 2, '[{"changed": {"fields": ["Quantity"]}}]', 7, 1);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.django_migrations VALUES (1, 'contenttypes', '0001_initial', '2025-05-28 19:24:43.802119+03');
INSERT INTO public.django_migrations VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2025-05-28 19:24:43.810578+03');
INSERT INTO public.django_migrations VALUES (3, 'auth', '0001_initial', '2025-05-28 19:24:43.840801+03');
INSERT INTO public.django_migrations VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2025-05-28 19:24:43.84954+03');
INSERT INTO public.django_migrations VALUES (5, 'auth', '0003_alter_user_email_max_length', '2025-05-28 19:24:43.861575+03');
INSERT INTO public.django_migrations VALUES (6, 'auth', '0004_alter_user_username_opts', '2025-05-28 19:24:43.898034+03');
INSERT INTO public.django_migrations VALUES (7, 'auth', '0005_alter_user_last_login_null', '2025-05-28 19:24:43.908576+03');
INSERT INTO public.django_migrations VALUES (8, 'auth', '0006_require_contenttypes_0002', '2025-05-28 19:24:43.91253+03');
INSERT INTO public.django_migrations VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2025-05-28 19:24:43.919528+03');
INSERT INTO public.django_migrations VALUES (10, 'auth', '0008_alter_user_username_max_length', '2025-05-28 19:24:43.927153+03');
INSERT INTO public.django_migrations VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2025-05-28 19:24:43.933557+03');
INSERT INTO public.django_migrations VALUES (12, 'auth', '0010_alter_group_name_max_length', '2025-05-28 19:24:43.941902+03');
INSERT INTO public.django_migrations VALUES (13, 'auth', '0011_update_proxy_permissions', '2025-05-28 19:24:43.948884+03');
INSERT INTO public.django_migrations VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2025-05-28 19:24:43.956443+03');
INSERT INTO public.django_migrations VALUES (15, 'userprofile', '0001_initial', '2025-05-28 19:24:43.991065+03');
INSERT INTO public.django_migrations VALUES (16, 'admin', '0001_initial', '2025-05-28 19:24:44.007212+03');
INSERT INTO public.django_migrations VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2025-05-28 19:24:44.018025+03');
INSERT INTO public.django_migrations VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-28 19:24:44.026924+03');
INSERT INTO public.django_migrations VALUES (19, 'sessions', '0001_initial', '2025-05-28 19:24:44.038724+03');
INSERT INTO public.django_migrations VALUES (20, 'store', '0001_initial', '2025-05-28 19:24:44.069484+03');
INSERT INTO public.django_migrations VALUES (21, 'store', '0002_initial', '2025-05-28 19:24:44.119765+03');
INSERT INTO public.django_migrations VALUES (22, 'store', '0003_rename_weight_ingredient_amount', '2025-05-28 19:32:20.599413+03');
INSERT INTO public.django_migrations VALUES (23, 'store', '0004_alter_order_total_amount', '2025-06-06 17:18:48.313768+03');
INSERT INTO public.django_migrations VALUES (24, 'store', '0005_order_refund_id', '2025-06-08 23:59:17.965097+03');
INSERT INTO public.django_migrations VALUES (25, 'userprofile', '0002_alter_userprofile_options_user_email_verified_at_and_more', '2025-06-14 15:09:26.107669+03');
INSERT INTO public.django_migrations VALUES (26, 'token_blacklist', '0001_initial', '2025-06-16 12:50:19.350244+03');
INSERT INTO public.django_migrations VALUES (27, 'token_blacklist', '0002_outstandingtoken_jti_hex', '2025-06-16 12:50:19.364009+03');
INSERT INTO public.django_migrations VALUES (28, 'token_blacklist', '0003_auto_20171017_2007', '2025-06-16 12:50:19.382261+03');
INSERT INTO public.django_migrations VALUES (29, 'token_blacklist', '0004_auto_20171017_2013', '2025-06-16 12:50:19.40064+03');
INSERT INTO public.django_migrations VALUES (30, 'token_blacklist', '0005_remove_outstandingtoken_jti', '2025-06-16 12:50:19.41534+03');
INSERT INTO public.django_migrations VALUES (31, 'token_blacklist', '0006_auto_20171017_2113', '2025-06-16 12:50:19.427742+03');
INSERT INTO public.django_migrations VALUES (32, 'token_blacklist', '0007_auto_20171017_2214', '2025-06-16 12:50:19.474295+03');
INSERT INTO public.django_migrations VALUES (33, 'token_blacklist', '0008_migrate_to_bigautofield', '2025-06-16 12:50:19.509436+03');
INSERT INTO public.django_migrations VALUES (34, 'token_blacklist', '0010_fix_migrate_to_bigautofield', '2025-06-16 12:50:19.527421+03');
INSERT INTO public.django_migrations VALUES (35, 'token_blacklist', '0011_linearizes_history', '2025-06-16 12:50:19.531375+03');
INSERT INTO public.django_migrations VALUES (36, 'token_blacklist', '0012_alter_outstandingtoken_user', '2025-06-16 12:50:19.545887+03');
INSERT INTO public.django_migrations VALUES (37, 'userprofile', '0003_alter_userprofile_options', '2025-06-16 12:50:19.558573+03');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.django_session VALUES ('2empnjmu0rxugu2q2phaubcbyuhg4kjt', 'eyJjYXJ0Ijp7fX0:1uRW71:4Ah0u6t4WZTHz7wolonG17Pz_iidGu9RIeKKMRCIKl8', '2025-06-18 16:12:27.591232+03');
INSERT INTO public.django_session VALUES ('uprqkbmb5x4ce5yyy75xrdpyyq7p9h0l', '.eJxVjEEOgyAUBe_C2hAQEHTZfc9APvAptkZTwEVjvHs1ceN2Zt7biIdcybDtDZmgVFsQsk_2u2L-kYEAaYiFtSa7Fsx2DAfj4g4d-A_OpwlvmF8L9ctc8-jomdDLFvpcAk6Pq70dJCjpWEseRR8DdtyItpOtMEoqVFpp7jQ4VIbJ1nShV8A091E4xhwLSjjHokEg-x-VQkMn:1uSAm9:SlXtSQM0zPfp5ec8oJfwsvIeJpnra6fIf491VcfpAdI', '2025-06-20 11:37:37.473691+03');


--
-- Data for Name: store_category; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.store_category VALUES (1, 'Emollients', 'emollients', '', true, '2025-05-28 19:26:06.421084+03');
INSERT INTO public.store_category VALUES (2, 'Surfactants', 'surfactants', '', true, '2025-05-28 19:26:13.198721+03');
INSERT INTO public.store_category VALUES (3, 'Dyes', 'dyes', '', true, '2025-05-28 19:26:18.355034+03');


--
-- Data for Name: store_ingredient; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.store_ingredient VALUES (2, 'Cetyl Alcohol', 'Многофункциональный косметический ингредиент с эмульгирующими и кондиционирующими свойствами. Несмотря на название "спирт", не обладает подсушивающим действием обычных спиртов.
Основные свойства:

Эмульгатор и стабилизатор эмульсий
Загуститель для кремов и лосьонов
Кондиционер для волос и кожи
Придает продуктам бархатистую текстуру

Применение:

Кремы и лосьоны для лица и тела
Шампуни и кондиционеры
Маски и бальзамы для волос
Декоративная косметика

Концентрация использования: 0,5-6% в зависимости от типа продукта
Преимущества:

Совместим с большинством косметических ингредиентов
Подходит для чувствительной кожи
Улучшает распределение и впитывание продукта
Стабилен при хранении

Идеален для создания питательных и увлажняющих формул с приятной консистенцией.', 'cetyl-alcohol', 'ingredients/2025/05/THK-CTAL-01-Cetyl-Alcohol-Front.jpg', 50.00, 0, 'g', 500.00, '2025-05-28 20:03:31.721742+03', '2025-06-03 20:06:44.473238+03', true, 1);
INSERT INTO public.store_ingredient VALUES (1, 'Sodium Lauryl Sulfate', 'Лаурилсульфат натрия (Sodium Lauryl Sulfate, SLS)
Анионное поверхностно-активное вещество с мощными очищающими и пенообразующими свойствами. Один из наиболее распространенных компонентов в индустрии персонального ухода.
Основные свойства:

Высокая моющая способность
Обильное пенообразование
Эмульгирующие свойства
Удаление жиров и загрязнений

Применение:

Шампуни и гели для душа
Зубные пасты
Очищающие средства для лица
Пены для ванн
Промышленные моющие средства

Концентрация использования: 5-40% в зависимости от продукта
особенности применения:

Может вызывать раздражение при высоких концентрациях
Рекомендуется комбинировать с мягкими ПАВ
Требует осторожного использования в средствах для чувствительной кожи
Эффективен в жесткой воде

Преимущества:

Отличное соотношение цена/качество
Стабильность в широком диапазоне pH
Совместимость с большинством ингредиентов

Подходит для создания эффективных очищающих продуктов с насыщенной пеной.', 'sodium-lauryl-sulfate', 'ingredients/2025/05/SRF-SLS-01-Sodium-Lauryl-Sulfate-Front_qawpjjQ.jpg', 100.00, 0, 'l', 1.00, '2025-05-28 20:02:12.616023+03', '2025-06-09 09:56:35.65089+03', true, 2);
INSERT INTO public.store_ingredient VALUES (4, 'Ethylhexyl Olivate', 'Натуральный эмолент, полученный из оливкового масла. Современная альтернатива силиконам с легкой, нежирной текстурой.
Основные свойства:

Легкий, быстро впитывающийся эмолент
Нежирная, шелковистая текстура
Хорошая растекаемость
Стабильность к окислению

Применение:

Кремы и лосьоны для лица и тела
Солнцезащитные средства
Основы под макияж
Сыворотки и масла для лица
Средства для массажа

Концентрация использования: 2-20% в зависимости от формулы
Ключевые преимущества:

Натуральное происхождение (из оливок)
Не оставляет жирного блеска
Совместим с широким спектром ингредиентов
Подходит для всех типов кожи
Улучшает сенсорные характеристики продукта

Особенности:

Отличная альтернатива циклометикону
Биоразлагаемый
Не комедогенный
Стабилен в различных pH', 'ethylhexyl-olivate', 'ingredients/2025/05/ELL-ETHXOL-01-Ethylhexyl-Olivate-Front.jpg', 66.33, 5, 'ml', 500.00, '2025-05-28 20:18:33.006764+03', '2025-06-09 22:52:29.196434+03', true, 1);
INSERT INTO public.store_ingredient VALUES (3, 'Amodimethicone', 'Амодиметикон (Amodimethicone)
Силиконовый полимер с аминофункциональными группами, специально разработанный для ухода за волосами. Обладает уникальными кондиционирующими и защитными свойствами.
Основные свойства:

Селективное прилипание к поврежденным участкам волос
Термозащитные свойства
Антистатический эффект
Придает блеск и гладкость

Применение:

Кондиционеры и маски для волос
Несмываемые средства для укладки
Термозащитные спреи
Сыворотки для поврежденных волос
Шампуни премиум-класса

Концентрация использования: 0,1-2% в зависимости от формулы
Ключевые преимущества:

Накапливается только на поврежденных участках
Не утяжеляет здоровые волосы
Облегчает расчесывание мокрых волос
Защищает от высоких температур при укладке
Уменьшает пушистость и электризацию

Особенности:

Водорастворим (в отличие от большинства силиконов)
Легко смывается обычным шампунем
Совместим с анионными ПАВ

Идеален для создания профессиональных средств по уходу за поврежденными и окрашенными волосами.', 'amodimethicone', 'ingredients/2025/05/ELL-AMDI-01-Amodimethicone-front.jpg', 20.00, 1, 'ml', 500.00, '2025-05-28 20:17:43.661254+03', '2025-06-09 07:52:09.445007+03', true, 2);
INSERT INTO public.store_ingredient VALUES (5, 'Beetroot Extract', 'Натуральный многофункциональный ингредиент, который действительно может использоваться как краситель, но обладает и другими полезными свойствами.
Основные функции:

Натуральный краситель (красно-фиолетовые оттенки)
Антиоксидант
Кондиционирующий агент
Увлажняющий компонент

Применение:

Декоративная косметика (помады, тинты, румяна)
Шампуни и кондиционеры для придания оттенка
Маски и кремы (как активный ингредиент)
Натуральные красители для волос
Средства для губ

Концентрация использования: 0,1-5% в зависимости от назначения
Активные компоненты:

Беталаины (природные пигменты)
Витамины группы B
Антиоксиданты
Минералы

Преимущества:

100% натуральное происхождение
Дополнительные ухаживающие свойства
Безопасен для чувствительной кожи
Стабильный цвет в нейтральном pH

Особенности:

Цвет может варьироваться от розового до темно-красного
Чувствителен к свету и высоким температурам
Лучше работает в водных фазах', 'beetroot-extract', 'ingredients/2025/05/PGNA-BEETRT-01-Beetroot-Extract-Pigment-Front.jpg', 15.66, 11, 'g', 200.00, '2025-05-28 20:20:49.77283+03', '2025-06-09 09:52:00.234305+03', true, 3);


--
-- Data for Name: store_order; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.store_order VALUES (3, 'Антон', 'Допіра', 'doublescreen509@gmail.com', '+38096666666', 'ул. Хряков', '49000', 'Dnipro', 'Ukraine', 50.00, 50.00, true, 'processing', 'pi_3RVyFpQoWZFQYpkK1fvJbtab', 'stripe', '2025-06-03 20:04:02.253684+03', '2025-06-03 20:06:44.466765+03', 2, '');
INSERT INTO public.store_order VALUES (9, 'Допіра', 'ddd', 'admin@gmail.com', '+38(097)-076-08-74', 'ыввы', '1234', 'Dnipro', 'Ukraine', 125.28, 125.28, true, 'cancelled', 'pi_3RXScUQoWZFQYpkK1Ua4DI7z', 'stripe', '2025-06-07 22:41:27.653283+03', '2025-06-07 22:42:02.032309+03', 1, '');
INSERT INTO public.store_order VALUES (10, 'Кайдаш', 'Вікторія', 'admin@gmail.com', '+38(097)-076-08-74', 'Семафорна 57', '49000', 'Dnipro', 'Ukraine', 156.60, 156.60, true, 'cancelled', 'pi_3RXflbQoWZFQYpkK1UKActtF', 'stripe', '2025-06-08 12:43:51.017098+03', '2025-06-08 12:52:18.507911+03', 1, '');
INSERT INTO public.store_order VALUES (26, 'Допіра', 'fff', 'admin@gmail.com', '+38(097)-076-08-74', 'ыввы', 'xxxxxxx', 'Dnipro', 'Ukraine', 20.00, 20.00, true, 'cancelled', 'pi_3RXxfAQoWZFQYpkK0FK2GtBO', 'stripe', '2025-06-09 07:50:23.644368+03', '2025-06-09 07:52:09.441084+03', 1, 're_3RXxfAQoWZFQYpkK0UhQQUY5');
INSERT INTO public.store_order VALUES (30, 'Допіра', 'fff', 'admin@gmail.com', '+38(097)-076-08-74', 'ыввы', '49000', 'Dnipro', 'Ukraine', 100.00, 100.00, true, 'processing', 'pi_3RXzd4QoWZFQYpkK0bEAPYkA', 'stripe', '2025-06-09 09:46:45.17729+03', '2025-06-09 09:56:35.644155+03', 1, '');
INSERT INTO public.store_order VALUES (22, 'Кайдаш', 'Вікторія', 'admin@gmail.com', '+38(097)-076-08-74', 'ыввы', 'aaaa', 'Dnipro', 'Ukraine', 312.30, 312.30, true, 'cancelled', 'pi_3RXpC1QoWZFQYpkK1CCBbSfq', 'stripe', '2025-06-08 22:47:45.922978+03', '2025-06-08 23:22:33.586445+03', 1, '');
INSERT INTO public.store_order VALUES (31, 'Допіра', 'Вікторія', 'admin@gmail.com', '+38(097)-076-08-74', 'Улица пушкина дом колотушкина', '49000', 'Dnipro', 'Ukraine', 66.33, 0.00, false, 'pending', 'pi_3RYBiTQoWZFQYpkK0ohq0NjW', 'stripe', '2025-06-09 22:50:45.543503+03', '2025-06-09 22:50:46.117558+03', NULL, '');
INSERT INTO public.store_order VALUES (32, 'Допіра', 'fff', 'doublescreen509@gmail.com', '+38(097)-076-08-74', 'Улица пушкина дом колотушкина', 'ssss', 'Dnipro', 'Ukraine', 66.33, 66.33, true, 'processing', 'pi_3RYBjuQoWZFQYpkK0nHjpuEZ', 'stripe', '2025-06-09 22:52:14.41726+03', '2025-06-09 22:52:29.188085+03', NULL, '');
INSERT INTO public.store_order VALUES (27, 'Кайдаш', 'Допіра', 'admin@gmail.com', '+38(097)-076-08-74', 'Улица пушкина дом колотушкина', '49000', 'Dnipro', 'Ukraine', 100.00, 0.00, false, 'cancelled', 'pi_3RXy1eQoWZFQYpkK0sUV9weg', 'stripe', '2025-06-09 08:13:28.226126+03', '2025-06-09 08:13:48.06525+03', 1, '');
INSERT INTO public.store_order VALUES (28, 'Допіра', 'Вікторія', 'admin@gmail.com', '+38(097)-076-08-74', 'Улица пушкина дом колотушкина', '49000', 'Киїів', 'Ukraine', 100.00, 100.00, true, 'cancelled', 'pi_3RXy2IQoWZFQYpkK1geKOlbd', 'stripe', '2025-06-09 08:14:17.895758+03', '2025-06-09 08:23:43.644687+03', 1, 're_3RXy2IQoWZFQYpkK1DYzWzqv');
INSERT INTO public.store_order VALUES (21, 'Допіра', 'Вікторія', 'admin@gmail.com', '+38(097)-076-08-74', 'ыввы', 'dddd', 'dsdssd', 'Ukraine', 312.30, 312.30, true, 'cancelled', 'pi_3RXyKfQoWZFQYpkK0LsFy5Gc', 'stripe', '2025-06-08 19:04:44.630389+03', '2025-06-09 08:33:40.166011+03', 1, 're_3RXyKfQoWZFQYpkK0SmmWUgY');
INSERT INTO public.store_order VALUES (29, 'Допіра', 'fff', 'admin@gmail.com', '+38(097)-076-08-74', 'ыввы', '1234', 'Dnipro', 'Ukraine', 15.66, 15.66, true, 'cancelled', 'pi_3RXyz1QoWZFQYpkK1GuK8rTh', 'stripe', '2025-06-09 09:14:59.006288+03', '2025-06-09 09:52:00.230082+03', 1, 're_3RXyz1QoWZFQYpkK1ICKIZKj');


--
-- Data for Name: store_orderitem; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.store_orderitem VALUES (4, 50.00, 1, 3, 2);
INSERT INTO public.store_orderitem VALUES (10, 15.66, 8, 9, 5);
INSERT INTO public.store_orderitem VALUES (11, 15.66, 10, 10, 5);
INSERT INTO public.store_orderitem VALUES (24, 15.66, 3, 21, 5);
INSERT INTO public.store_orderitem VALUES (25, 66.33, 4, 21, 4);
INSERT INTO public.store_orderitem VALUES (26, 15.66, 3, 22, 5);
INSERT INTO public.store_orderitem VALUES (27, 66.33, 4, 22, 4);
INSERT INTO public.store_orderitem VALUES (31, 20.00, 1, 26, 3);
INSERT INTO public.store_orderitem VALUES (32, 100.00, 1, 27, 1);
INSERT INTO public.store_orderitem VALUES (33, 100.00, 1, 28, 1);
INSERT INTO public.store_orderitem VALUES (34, 15.66, 1, 29, 5);
INSERT INTO public.store_orderitem VALUES (35, 100.00, 1, 30, 1);
INSERT INTO public.store_orderitem VALUES (36, 66.33, 1, 31, 4);
INSERT INTO public.store_orderitem VALUES (37, 66.33, 1, 32, 4);


--
-- Data for Name: token_blacklist_outstandingtoken; Type: TABLE DATA; Schema: public; Owner: antond
--



--
-- Data for Name: token_blacklist_blacklistedtoken; Type: TABLE DATA; Schema: public; Owner: antond
--



--
-- Data for Name: userprofile_user_groups; Type: TABLE DATA; Schema: public; Owner: antond
--



--
-- Data for Name: userprofile_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: antond
--



--
-- Data for Name: userprofile_userprofile; Type: TABLE DATA; Schema: public; Owner: antond
--

INSERT INTO public.userprofile_userprofile VALUES (2, 'ул. Хряков', '+38096666666', 'images/AntonTheMighty/Снимок_экрана_2023-11-26_153325.png', 2, '2025-06-14 15:09:26.067384+03', '2025-06-14 15:09:26.08203+03');
INSERT INTO public.userprofile_userprofile VALUES (1, 'Улица пушкина дом колотушкина', '+380970760874', 'images/admin/Снимок_экрана_2023-11-26_153325.png', 1, '2025-06-14 15:09:26.067384+03', '2025-06-14 15:09:26.08203+03');
INSERT INTO public.userprofile_userprofile VALUES (43, NULL, NULL, '', 13, '2025-06-16 12:56:00.970257+03', '2025-06-16 12:56:00.970558+03');


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 42, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 37, true);


--
-- Name: store_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.store_category_id_seq', 3, true);


--
-- Name: store_ingredient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.store_ingredient_id_seq', 37, true);


--
-- Name: store_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.store_order_id_seq', 32, true);


--
-- Name: store_orderitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.store_orderitem_id_seq', 37, true);


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.token_blacklist_blacklistedtoken_id_seq', 1, false);


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.token_blacklist_outstandingtoken_id_seq', 1, false);


--
-- Name: userprofile_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.userprofile_user_groups_id_seq', 1, false);


--
-- Name: userprofile_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.userprofile_user_id_seq', 13, true);


--
-- Name: userprofile_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.userprofile_user_user_permissions_id_seq', 1, false);


--
-- Name: userprofile_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: antond
--

SELECT pg_catalog.setval('public.userprofile_userprofile_id_seq', 43, true);


--
-- PostgreSQL database dump complete
--

