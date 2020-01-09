
typedef struct state_list {
	state* state;
	state_list* next;
} state_list;

typedef struct state {
	void* partitions;
	state_list* vert;
	state_list* horiz;
	state_list* ivs;
} state;

void vert(state* s){

}