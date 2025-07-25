PGDMP  "                    }            BAR2025    17.4    17.4 (    &           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            '           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            (           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            )           1262    16389    BAR2025    DATABASE     o   CREATE DATABASE "BAR2025" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es-MX';
    DROP DATABASE "BAR2025";
                     postgres    false            �            1259    16535 
   categorias    TABLE     u   CREATE TABLE public.categorias (
    id_categoria integer NOT NULL,
    categoria character varying(100) NOT NULL
);
    DROP TABLE public.categorias;
       public         heap r       postgres    false            �            1259    16534    categorias_id_categoria_seq    SEQUENCE     �   CREATE SEQUENCE public.categorias_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.categorias_id_categoria_seq;
       public               postgres    false    225            *           0    0    categorias_id_categoria_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.categorias_id_categoria_seq OWNED BY public.categorias.id_categoria;
          public               postgres    false    224            �            1259    16490    detalle_venta    TABLE     u  CREATE TABLE public.detalle_venta (
    id_detalle integer NOT NULL,
    id_venta integer NOT NULL,
    id_producto integer NOT NULL,
    cantidad integer NOT NULL,
    precio_unitario numeric(10,2) NOT NULL,
    CONSTRAINT detalle_venta_cantidad_check CHECK ((cantidad > 0)),
    CONSTRAINT detalle_venta_precio_unitario_check CHECK ((precio_unitario >= (0)::numeric))
);
 !   DROP TABLE public.detalle_venta;
       public         heap r       postgres    false            �            1259    16489    detalle_venta_id_detalle_seq    SEQUENCE     �   CREATE SEQUENCE public.detalle_venta_id_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.detalle_venta_id_detalle_seq;
       public               postgres    false    221            +           0    0    detalle_venta_id_detalle_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.detalle_venta_id_detalle_seq OWNED BY public.detalle_venta.id_detalle;
          public               postgres    false    220            �            1259    16517 	   productos    TABLE     C  CREATE TABLE public.productos (
    id integer NOT NULL,
    id_producto character varying(20) NOT NULL,
    nombre_producto character varying(100) NOT NULL,
    cantidad_stock integer NOT NULL,
    costo_unitario real NOT NULL,
    limite_alarmante integer NOT NULL,
    id_categoria integer NOT NULL,
    estado character varying(20) DEFAULT 'disponible'::character varying,
    CONSTRAINT productos_cantidad_stock_check CHECK ((cantidad_stock >= 0)),
    CONSTRAINT productos_costo_unitario_check CHECK ((costo_unitario >= ((0)::numeric)::double precision)),
    CONSTRAINT productos_estado_check CHECK (((estado)::text = ANY ((ARRAY['disponible'::character varying, 'no disponible'::character varying, 'stock bajo'::character varying])::text[]))),
    CONSTRAINT productos_limite_alarmante_check CHECK ((limite_alarmante >= 0))
);
    DROP TABLE public.productos;
       public         heap r       postgres    false            �            1259    16516    productos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.productos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.productos_id_seq;
       public               postgres    false    223            ,           0    0    productos_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.productos_id_seq OWNED BY public.productos.id;
          public               postgres    false    222            �            1259    16443    usuarios    TABLE     �  CREATE TABLE public.usuarios (
    dni_usuario character varying(20) NOT NULL,
    nombre character varying(100) NOT NULL,
    tipo_usuario character varying(20) NOT NULL,
    fecha_nacimiento date NOT NULL,
    clave text NOT NULL,
    estado character varying(20) DEFAULT 'activo'::character varying NOT NULL,
    CONSTRAINT chk_estado_usuario CHECK (((estado)::text = ANY ((ARRAY['activo'::character varying, 'inactivo'::character varying, 'suspendido'::character varying])::text[]))),
    CONSTRAINT usuarios_tipo_usuario_check CHECK (((tipo_usuario)::text = ANY ((ARRAY['camarero'::character varying, 'vendedor'::character varying, 'administrador'::character varying, 'cajero'::character varying])::text[])))
);
    DROP TABLE public.usuarios;
       public         heap r       postgres    false            �            1259    16477    ventas    TABLE     3  CREATE TABLE public.ventas (
    id_venta integer NOT NULL,
    dni_usuario character varying(20) NOT NULL,
    valor_total numeric(10,2) NOT NULL,
    fecha_venta date NOT NULL,
    forma_pago character varying(50) NOT NULL,
    CONSTRAINT ventas_valor_total_check CHECK ((valor_total >= (0)::numeric))
);
    DROP TABLE public.ventas;
       public         heap r       postgres    false            �            1259    16476    ventas_id_venta_seq    SEQUENCE     �   CREATE SEQUENCE public.ventas_id_venta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.ventas_id_venta_seq;
       public               postgres    false    219            -           0    0    ventas_id_venta_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.ventas_id_venta_seq OWNED BY public.ventas.id_venta;
          public               postgres    false    218            o           2604    16538    categorias id_categoria    DEFAULT     �   ALTER TABLE ONLY public.categorias ALTER COLUMN id_categoria SET DEFAULT nextval('public.categorias_id_categoria_seq'::regclass);
 F   ALTER TABLE public.categorias ALTER COLUMN id_categoria DROP DEFAULT;
       public               postgres    false    224    225    225            l           2604    16493    detalle_venta id_detalle    DEFAULT     �   ALTER TABLE ONLY public.detalle_venta ALTER COLUMN id_detalle SET DEFAULT nextval('public.detalle_venta_id_detalle_seq'::regclass);
 G   ALTER TABLE public.detalle_venta ALTER COLUMN id_detalle DROP DEFAULT;
       public               postgres    false    221    220    221            m           2604    16520    productos id    DEFAULT     l   ALTER TABLE ONLY public.productos ALTER COLUMN id SET DEFAULT nextval('public.productos_id_seq'::regclass);
 ;   ALTER TABLE public.productos ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    222    223    223            k           2604    16480    ventas id_venta    DEFAULT     r   ALTER TABLE ONLY public.ventas ALTER COLUMN id_venta SET DEFAULT nextval('public.ventas_id_venta_seq'::regclass);
 >   ALTER TABLE public.ventas ALTER COLUMN id_venta DROP DEFAULT;
       public               postgres    false    219    218    219            #          0    16535 
   categorias 
   TABLE DATA           =   COPY public.categorias (id_categoria, categoria) FROM stdin;
    public               postgres    false    225   c4                 0    16490    detalle_venta 
   TABLE DATA           e   COPY public.detalle_venta (id_detalle, id_venta, id_producto, cantidad, precio_unitario) FROM stdin;
    public               postgres    false    221   �4       !          0    16517 	   productos 
   TABLE DATA           �   COPY public.productos (id, id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria, estado) FROM stdin;
    public               postgres    false    223   ;5                 0    16443    usuarios 
   TABLE DATA           f   COPY public.usuarios (dni_usuario, nombre, tipo_usuario, fecha_nacimiento, clave, estado) FROM stdin;
    public               postgres    false    217   6                 0    16477    ventas 
   TABLE DATA           ]   COPY public.ventas (id_venta, dni_usuario, valor_total, fecha_venta, forma_pago) FROM stdin;
    public               postgres    false    219   �8       .           0    0    categorias_id_categoria_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.categorias_id_categoria_seq', 8, true);
          public               postgres    false    224            /           0    0    detalle_venta_id_detalle_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.detalle_venta_id_detalle_seq', 12, true);
          public               postgres    false    220            0           0    0    productos_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.productos_id_seq', 25, true);
          public               postgres    false    222            1           0    0    ventas_id_venta_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.ventas_id_venta_seq', 1, false);
          public               postgres    false    218            �           2606    16542 #   categorias categorias_categoria_key 
   CONSTRAINT     c   ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_categoria_key UNIQUE (categoria);
 M   ALTER TABLE ONLY public.categorias DROP CONSTRAINT categorias_categoria_key;
       public                 postgres    false    225            �           2606    16540    categorias categorias_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria);
 D   ALTER TABLE ONLY public.categorias DROP CONSTRAINT categorias_pkey;
       public                 postgres    false    225            ~           2606    16497     detalle_venta detalle_venta_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_pkey PRIMARY KEY (id_detalle);
 J   ALTER TABLE ONLY public.detalle_venta DROP CONSTRAINT detalle_venta_pkey;
       public                 postgres    false    221            �           2606    16527 #   productos productos_id_producto_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_id_producto_key UNIQUE (id_producto);
 M   ALTER TABLE ONLY public.productos DROP CONSTRAINT productos_id_producto_key;
       public                 postgres    false    223            �           2606    16525    productos productos_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.productos DROP CONSTRAINT productos_pkey;
       public                 postgres    false    223            z           2606    16450    usuarios usuarios_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (dni_usuario);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public                 postgres    false    217            |           2606    16483    ventas ventas_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY (id_venta);
 <   ALTER TABLE ONLY public.ventas DROP CONSTRAINT ventas_pkey;
       public                 postgres    false    219            �           2606    16484    ventas fk_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT fk_usuario FOREIGN KEY (dni_usuario) REFERENCES public.usuarios(dni_usuario);
 ;   ALTER TABLE ONLY public.ventas DROP CONSTRAINT fk_usuario;
       public               postgres    false    217    4730    219            �           2606    16498    detalle_venta fk_venta    FK CONSTRAINT     }   ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT fk_venta FOREIGN KEY (id_venta) REFERENCES public.ventas(id_venta);
 @   ALTER TABLE ONLY public.detalle_venta DROP CONSTRAINT fk_venta;
       public               postgres    false    221    219    4732            �           2606    16543    productos id_categoria    FK CONSTRAINT     �   ALTER TABLE ONLY public.productos
    ADD CONSTRAINT id_categoria FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria);
 @   ALTER TABLE ONLY public.productos DROP CONSTRAINT id_categoria;
       public               postgres    false    225    223    4742            #   Y   x�3��*M�/�2�tN-*K�J,�2���
�p�gdgW�s�r��d��8CRK3s�LsN�����b ӂӱ �(�$��-F��� �g�         _   x�U��� D�P�
~zI�ud1cƋ��*UR�%"E�+�m<E��ُ=8#E���L�#g�9:j��{�
D��#p�ym@�G����0��FU      !   �   x�U�=�0���=���o.Bb��Ŕ "ڤj��hY�O��T�q��U��;;� UJ)T0��u��F[Pb��Ž-ؠI��L��u޾�3ڄ��ڂ{;���t�uQFh�\�@-8�ފϓ[|x<�;�	UҨ��$�3�&�L��6�Ys~״�W�>Ra�BU���Uܜć�쿎��3��� C�a         �  x����v�@�5>�lE���"xA�W�lZ�4���s̋j0z�]2�*v�鿪�</������"/���NP� gǲl�� P/��p/�۬���W��Z*9-4B" �:2{������.�^h���P����":�FeUb[�L�%����?0 �&4Wc���{�Nn�>�w�w��?ر�aزx�N�i�0�R��<<���%S�"�R��	�?C�w�
�\R$�����R�.�/��8J��ȼ'�gR�u���K|L��ϻs+9����Ei��CH�&�`��w��u�,[�T��Kw��ѽw��{�$�����{[��/�ld�#�\8#u�jņg�9�	�$���F�b�kYV�ke~�$�zK�������eN��+
p�*K!�I����}�9�
������s��>���N��t�����V#\�rq��})j-T$.A�|7|O���3tBO��;C)^��o����jx�ۣ�cO���1��L�I߯-�Q��-S��,0���{�mQX�+���z���/9j���ȣo�	l7�v�kנ�0���رq<�R�b�ɐ��$���,�9���6�=��c�������R�xSa�Z�YI��	��=�>r]%֍��Pُ���tD�3ܤL��hGq2��9����j�b��?VZ��         _   x�3�464153���400�30�4202�50�52�I,�J-ITHIUp.:�2%�$�ˈX.�W&�4#4�����Ă8W�"���%F��� �oA     